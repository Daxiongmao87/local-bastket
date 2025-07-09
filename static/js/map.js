/**
 * Map functionality for Local Basket application
 */

class MapService {
  constructor() {
    this.map = null;
    this.markers = [];
    this.userMarker = null;
    this.mapContainer = null;
    this.defaultCenter = { lat: 40.7128, lng: -74.0060 }; // New York City
    this.defaultZoom = 10;
  }

  /**
   * Initialize map
   * @param {string} containerId - Map container element ID
   * @param {Object} options - Map options
   * @returns {Promise<void>}
   */
  async init(containerId, options = {}) {
    this.mapContainer = document.getElementById(containerId);
    if (!this.mapContainer) {
      throw new Error(`Map container with ID '${containerId}' not found`);
    }

    const mapOptions = {
      center: options.center || this.defaultCenter,
      zoom: options.zoom || this.defaultZoom,
      ...options
    };

    // Check if we can use a real map service or fallback to placeholder
    if (this.isMapServiceAvailable()) {
      await this.initRealMap(mapOptions);
    } else {
      this.initPlaceholderMap(mapOptions);
    }
  }

  /**
   * Check if map service is available
   * @returns {boolean} Is map service available
   */
  isMapServiceAvailable() {
    // Check if Google Maps API is loaded
    return typeof google !== 'undefined' && google.maps;
  }

  /**
   * Initialize real map (Google Maps)
   * @param {Object} options - Map options
   * @returns {Promise<void>}
   */
  async initRealMap(options) {
    try {
      this.map = new google.maps.Map(this.mapContainer, options);
      
      // Add click event listener
      this.map.addListener('click', (event) => {
        this.onMapClick(event);
      });

      // Load shops on map
      await this.loadShops();
      
      // Try to center on user location
      this.centerOnUserLocation();
      
    } catch (error) {
      console.error('Failed to initialize Google Maps:', error);
      this.initPlaceholderMap(options);
    }
  }

  /**
   * Initialize placeholder map
   * @param {Object} options - Map options
   */
  initPlaceholderMap(options) {
    this.mapContainer.innerHTML = `
      <div class="map-placeholder">
        <div class="map-placeholder-content">
          <i class="fas fa-map-marked-alt" style="font-size: 3rem; margin-bottom: 1rem;"></i>
          <h3>Interactive Map</h3>
          <p>Shop locations will appear here when map service is available</p>
          <button class="btn btn-primary" onclick="MapService.requestUserLocation()">
            <i class="fas fa-location-arrow"></i> Find My Location
          </button>
        </div>
      </div>
    `;
    
    this.mapContainer.style.display = 'flex';
    this.mapContainer.style.alignItems = 'center';
    this.mapContainer.style.justifyContent = 'center';
  }

  /**
   * Load shops on map
   * @returns {Promise<void>}
   */
  async loadShops() {
    try {
      const response = await fetch('/api/shops');
      const shops = await response.json();
      
      this.clearMarkers();
      
      shops.forEach(shop => {
        this.addShopMarker(shop);
      });
      
    } catch (error) {
      console.error('Failed to load shops:', error);
      Utils.showToast('Failed to load shop locations', 'error');
    }
  }

  /**
   * Add shop marker to map
   * @param {Object} shop - Shop data
   */
  addShopMarker(shop) {
    if (!this.map) return;

    const marker = new google.maps.Marker({
      position: { lat: shop.latitude, lng: shop.longitude },
      map: this.map,
      title: shop.name,
      icon: {
        url: this.getShopIcon(shop),
        scaledSize: new google.maps.Size(40, 40)
      }
    });

    const infoWindow = new google.maps.InfoWindow({
      content: this.createInfoWindowContent(shop)
    });

    marker.addListener('click', () => {
      this.closeAllInfoWindows();
      infoWindow.open(this.map, marker);
    });

    this.markers.push({ marker, infoWindow, shop });
  }

  /**
   * Get shop icon based on status
   * @param {Object} shop - Shop data
   * @returns {string} Icon URL
   */
  getShopIcon(shop) {
    const baseUrl = '/static/images/markers/';
    return shop.is_open ? `${baseUrl}shop-open.png` : `${baseUrl}shop-closed.png`;
  }

  /**
   * Create info window content
   * @param {Object} shop - Shop data
   * @returns {string} HTML content
   */
  createInfoWindowContent(shop) {
    const status = shop.is_open ? 'Open' : 'Closed';
    const statusClass = shop.is_open ? 'text-success' : 'text-error';
    const rating = shop.rating || 0;
    const stars = Utils.generateStars(rating);
    
    return `
      <div class="shop-info-window">
        <h4>${Utils.sanitizeHTML(shop.name)}</h4>
        <p class="${statusClass}">
          <i class="fas fa-circle"></i> ${status}
        </p>
        <div class="rating">
          ${stars} (${rating.toFixed(1)})
        </div>
        <p class="address">
          <i class="fas fa-map-marker-alt"></i> ${Utils.sanitizeHTML(shop.address)}
        </p>
        <div class="info-actions">
          <a href="/shop/${shop.id}" class="btn btn-primary btn-sm">
            <i class="fas fa-store"></i> View Shop
          </a>
          <button onclick="MapService.getDirections(${shop.latitude}, ${shop.longitude})" 
                  class="btn btn-outline-primary btn-sm">
            <i class="fas fa-directions"></i> Directions
          </button>
        </div>
      </div>
    `;
  }

  /**
   * Center map on user location
   */
  async centerOnUserLocation() {
    try {
      const position = await GeolocationService.getCurrentPosition();
      const userLat = position.coords.latitude;
      const userLng = position.coords.longitude;
      
      if (this.map) {
        this.map.setCenter({ lat: userLat, lng: userLng });
        this.map.setZoom(13);
        
        // Add user marker
        this.addUserMarker(userLat, userLng);
      }
      
    } catch (error) {
      console.warn('Could not center on user location:', error.message);
    }
  }

  /**
   * Add user location marker
   * @param {number} lat - Latitude
   * @param {number} lng - Longitude
   */
  addUserMarker(lat, lng) {
    if (!this.map) return;

    // Remove existing user marker
    if (this.userMarker) {
      this.userMarker.setMap(null);
    }

    this.userMarker = new google.maps.Marker({
      position: { lat, lng },
      map: this.map,
      title: 'Your Location',
      icon: {
        url: '/static/images/markers/user-location.png',
        scaledSize: new google.maps.Size(30, 30)
      }
    });
  }

  /**
   * Clear all markers
   */
  clearMarkers() {
    this.markers.forEach(({ marker }) => {
      marker.setMap(null);
    });
    this.markers = [];
  }

  /**
   * Close all info windows
   */
  closeAllInfoWindows() {
    this.markers.forEach(({ infoWindow }) => {
      infoWindow.close();
    });
  }

  /**
   * Handle map click
   * @param {Object} event - Map click event
   */
  onMapClick(event) {
    this.closeAllInfoWindows();
  }

  /**
   * Filter shops by distance
   * @param {number} maxDistance - Maximum distance in km
   */
  async filterByDistance(maxDistance) {
    try {
      const userLocation = await GeolocationService.getUserLocation();
      const response = await fetch('/api/shops');
      const shops = await response.json();
      
      const filteredShops = shops.filter(shop => {
        const distance = GeolocationService.calculateDistance(
          userLocation.latitude,
          userLocation.longitude,
          shop.latitude,
          shop.longitude
        );
        return distance <= maxDistance;
      });
      
      this.clearMarkers();
      filteredShops.forEach(shop => {
        this.addShopMarker(shop);
      });
      
    } catch (error) {
      console.error('Failed to filter shops by distance:', error);
    }
  }

  /**
   * Search shops on map
   * @param {string} query - Search query
   */
  async searchShops(query) {
    try {
      const response = await fetch(`/api/shops?search=${encodeURIComponent(query)}`);
      const shops = await response.json();
      
      this.clearMarkers();
      shops.forEach(shop => {
        this.addShopMarker(shop);
      });
      
      // Fit map to show all markers
      if (shops.length > 0) {
        this.fitToMarkers();
      }
      
    } catch (error) {
      console.error('Failed to search shops:', error);
    }
  }

  /**
   * Fit map to show all markers
   */
  fitToMarkers() {
    if (!this.map || this.markers.length === 0) return;

    const bounds = new google.maps.LatLngBounds();
    this.markers.forEach(({ marker }) => {
      bounds.extend(marker.getPosition());
    });
    
    this.map.fitBounds(bounds);
  }

  /**
   * Get directions to shop
   * @param {number} lat - Shop latitude
   * @param {number} lng - Shop longitude
   */
  static getDirections(lat, lng) {
    const url = `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}`;
    window.open(url, '_blank');
  }

  /**
   * Request user location (for placeholder map)
   */
  static async requestUserLocation() {
    try {
      const position = await GeolocationService.getCurrentPosition();
      Utils.showToast('Location found! Redirecting to map...', 'success');
      
      // Refresh page to reload map with location
      setTimeout(() => {
        window.location.reload();
      }, 1000);
      
    } catch (error) {
      Utils.showToast(`Location error: ${error.message}`, 'error');
    }
  }

  /**
   * Initialize map controls
   */
  initControls() {
    const controlsContainer = document.getElementById('map-controls');
    if (!controlsContainer) return;

    controlsContainer.innerHTML = `
      <div class="map-controls">
        <div class="control-group">
          <label for="distance-filter">Filter by Distance:</label>
          <select id="distance-filter" class="form-control">
            <option value="">All Shops</option>
            <option value="5">Within 5 km</option>
            <option value="10">Within 10 km</option>
            <option value="25">Within 25 km</option>
            <option value="50">Within 50 km</option>
          </select>
        </div>
        <div class="control-group">
          <label for="shop-search">Search Shops:</label>
          <input type="text" id="shop-search" class="form-control" placeholder="Search shops...">
        </div>
        <div class="control-group">
          <button id="locate-me" class="btn btn-primary">
            <i class="fas fa-location-arrow"></i> Find My Location
          </button>
        </div>
      </div>
    `;

    // Add event listeners
    document.getElementById('distance-filter').addEventListener('change', (e) => {
      const distance = e.target.value;
      if (distance) {
        this.filterByDistance(parseInt(distance));
      } else {
        this.loadShops();
      }
    });

    document.getElementById('shop-search').addEventListener('input', 
      Utils.debounce((e) => {
        const query = e.target.value;
        if (query) {
          this.searchShops(query);
        } else {
          this.loadShops();
        }
      }, 300)
    );

    document.getElementById('locate-me').addEventListener('click', () => {
      this.centerOnUserLocation();
    });
  }
}

// Create global instance
window.MapService = new MapService();