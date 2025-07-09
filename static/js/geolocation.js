/**
 * Geolocation service for Local Basket application
 */

class GeolocationService {
  constructor() {
    this.userLocation = null;
    this.watchId = null;
    this.options = {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 300000 // 5 minutes
    };
  }

  /**
   * Check if geolocation is supported
   * @returns {boolean} Is geolocation supported
   */
  isSupported() {
    return 'geolocation' in navigator;
  }

  /**
   * Get current position
   * @returns {Promise<GeolocationPosition>} Current position
   */
  getCurrentPosition() {
    return new Promise((resolve, reject) => {
      if (!this.isSupported()) {
        reject(new Error('Geolocation is not supported by this browser'));
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          this.userLocation = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            accuracy: position.coords.accuracy,
            timestamp: position.timestamp
          };
          resolve(position);
        },
        (error) => {
          reject(this.handleLocationError(error));
        },
        this.options
      );
    });
  }

  /**
   * Watch position changes
   * @param {Function} successCallback - Success callback
   * @param {Function} errorCallback - Error callback
   * @returns {number} Watch ID
   */
  watchPosition(successCallback, errorCallback) {
    if (!this.isSupported()) {
      errorCallback(new Error('Geolocation is not supported by this browser'));
      return null;
    }

    this.watchId = navigator.geolocation.watchPosition(
      (position) => {
        this.userLocation = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          accuracy: position.coords.accuracy,
          timestamp: position.timestamp
        };
        successCallback(position);
      },
      (error) => {
        errorCallback(this.handleLocationError(error));
      },
      this.options
    );

    return this.watchId;
  }

  /**
   * Stop watching position
   */
  stopWatching() {
    if (this.watchId !== null) {
      navigator.geolocation.clearWatch(this.watchId);
      this.watchId = null;
    }
  }

  /**
   * Handle location errors
   * @param {GeolocationPositionError} error - Geolocation error
   * @returns {Error} Formatted error
   */
  handleLocationError(error) {
    let message;
    switch (error.code) {
      case error.PERMISSION_DENIED:
        message = 'Location access denied by user';
        break;
      case error.POSITION_UNAVAILABLE:
        message = 'Location information is unavailable';
        break;
      case error.TIMEOUT:
        message = 'Location request timed out';
        break;
      default:
        message = 'An unknown error occurred while retrieving location';
        break;
    }
    return new Error(message);
  }

  /**
   * Calculate distance between two points
   * @param {number} lat1 - Latitude of first point
   * @param {number} lon1 - Longitude of first point
   * @param {number} lat2 - Latitude of second point
   * @param {number} lon2 - Longitude of second point
   * @param {string} unit - Unit (km or mi)
   * @returns {number} Distance
   */
  calculateDistance(lat1, lon1, lat2, lon2, unit = 'km') {
    const R = unit === 'km' ? 6371 : 3959; // Earth's radius in km or miles
    const dLat = this.toRadians(lat2 - lat1);
    const dLon = this.toRadians(lon2 - lon1);
    const a = 
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(this.toRadians(lat1)) * Math.cos(this.toRadians(lat2)) *
      Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }

  /**
   * Convert degrees to radians
   * @param {number} degrees - Degrees to convert
   * @returns {number} Radians
   */
  toRadians(degrees) {
    return degrees * (Math.PI / 180);
  }

  /**
   * Get user's location or use default
   * @param {Object} defaultLocation - Default location {latitude, longitude}
   * @returns {Promise<Object>} User location
   */
  async getUserLocation(defaultLocation = { latitude: 40.7128, longitude: -74.0060 }) {
    try {
      const position = await this.getCurrentPosition();
      return {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        accuracy: position.coords.accuracy,
        source: 'geolocation'
      };
    } catch (error) {
      console.warn('Failed to get user location:', error.message);
      return {
        ...defaultLocation,
        source: 'default'
      };
    }
  }

  /**
   * Sort locations by distance from user
   * @param {Array} locations - Array of locations with latitude/longitude
   * @param {Object} userLocation - User's location
   * @param {string} unit - Unit (km or mi)
   * @returns {Array} Sorted locations with distance
   */
  sortByDistance(locations, userLocation, unit = 'km') {
    if (!userLocation) {
      return locations.map(location => ({ ...location, distance: null }));
    }

    return locations
      .map(location => ({
        ...location,
        distance: this.calculateDistance(
          userLocation.latitude,
          userLocation.longitude,
          location.latitude,
          location.longitude,
          unit
        )
      }))
      .sort((a, b) => (a.distance || Infinity) - (b.distance || Infinity));
  }

  /**
   * Filter locations within radius
   * @param {Array} locations - Array of locations
   * @param {Object} userLocation - User's location
   * @param {number} radius - Radius in specified unit
   * @param {string} unit - Unit (km or mi)
   * @returns {Array} Filtered locations
   */
  filterByRadius(locations, userLocation, radius, unit = 'km') {
    if (!userLocation) {
      return locations;
    }

    return locations.filter(location => {
      const distance = this.calculateDistance(
        userLocation.latitude,
        userLocation.longitude,
        location.latitude,
        location.longitude,
        unit
      );
      return distance <= radius;
    });
  }

  /**
   * Request location permission
   * @returns {Promise<string>} Permission state
   */
  async requestPermission() {
    if (!this.isSupported()) {
      return 'not-supported';
    }

    try {
      const permission = await navigator.permissions.query({ name: 'geolocation' });
      return permission.state;
    } catch (error) {
      // Fallback: try to get position to trigger permission request
      try {
        await this.getCurrentPosition();
        return 'granted';
      } catch (positionError) {
        return 'denied';
      }
    }
  }

  /**
   * Get location from address using geocoding
   * @param {string} address - Address to geocode
   * @returns {Promise<Object>} Location coordinates
   */
  async geocodeAddress(address) {
    try {
      const response = await fetch(`/api/geocode?address=${encodeURIComponent(address)}`);
      if (!response.ok) {
        throw new Error('Geocoding failed');
      }
      const data = await response.json();
      return {
        latitude: data.latitude,
        longitude: data.longitude,
        source: 'geocoding'
      };
    } catch (error) {
      throw new Error(`Failed to geocode address: ${error.message}`);
    }
  }

  /**
   * Get address from coordinates using reverse geocoding
   * @param {number} latitude - Latitude
   * @param {number} longitude - Longitude
   * @returns {Promise<string>} Address string
   */
  async reverseGeocode(latitude, longitude) {
    try {
      const response = await fetch(`/api/reverse-geocode?lat=${latitude}&lng=${longitude}`);
      if (!response.ok) {
        throw new Error('Reverse geocoding failed');
      }
      const data = await response.json();
      return data.address;
    } catch (error) {
      throw new Error(`Failed to reverse geocode: ${error.message}`);
    }
  }

  /**
   * Get cached user location
   * @returns {Object|null} Cached location
   */
  getCachedLocation() {
    return this.userLocation;
  }

  /**
   * Clear cached location
   */
  clearCachedLocation() {
    this.userLocation = null;
  }
}

// Create global instance
window.GeolocationService = new GeolocationService();