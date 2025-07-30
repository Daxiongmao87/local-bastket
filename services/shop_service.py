from datetime import datetime
from models import db, Shop

class ShopService:
    """Service class for shop-related operations."""

    def update_shop_statuses(self):
        """
        Update the open/closed status of shops based on their operating hours.
        This function is intended to be run by a scheduler.
        """
        now = datetime.now()
        current_day_index = now.weekday() # Monday is 0, Sunday is 6
        current_time = now.time()

        # Map weekday index to the correct model field
        day_mapping = {
            0: 'hours_monday',
            1: 'hours_tuesday',
            2: 'hours_wednesday',
            3: 'hours_thursday',
            4: 'hours_friday',
            5: 'hours_saturday',
            6: 'hours_sunday'
        }
        
        field_name = day_mapping.get(current_day_index)
        if not field_name:
            return

        # Get all shops that have hours defined for the current day and are not manually overridden
        shops_to_check = Shop.query.filter(
            Shop.manual_override == False,
            getattr(Shop, field_name) != None,
            getattr(Shop, field_name) != ''
        ).all()

        for shop in shops_to_check:
            hours_str = getattr(shop, field_name)
            try:
                # Assuming format "HH:MM-HH:MM" (e.g., "09:00-17:00")
                open_time_str, close_time_str = hours_str.split('-')
                open_time = datetime.strptime(open_time_str, '%H:%M').time()
                close_time = datetime.strptime(close_time_str, '%H:%M').time()

                if open_time <= current_time < close_time:
                    shop.is_open = True
                else:
                    shop.is_open = False
            except (ValueError, TypeError):
                # If parsing fails, do nothing and possibly log the error
                continue
        
        db.session.commit()

shop_service = ShopService()
