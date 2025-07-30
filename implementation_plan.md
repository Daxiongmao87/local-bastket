# Implementation Plan for Missing Features

This document outlines the steps to implement the missing features identified during the code review.

## 1. Automated Shop Open/Closed Status

This feature will automatically set a shop's status to "open" or "closed" based on the operating hours provided by the seller.

### Step 1: Add a Scheduler
- Integrate a lightweight scheduler like `APScheduler`.
- Add `APScheduler` to `requirements.txt`.
- Configure the scheduler in `app.py` to run a daily job.

### Step 2: Create a Status Update Job
- Create a new function in `services/shop_service.py` (a new file to be created) called `update_shop_statuses`.
- This function will:
    - Query all shops that have defined operating hours.
    - For each shop, get the current day of the week and time.
    - Parse the shop's hours for the current day (e.g., "9:00-17:00").
    - Compare the current time to the opening and closing times.
    - Update the `is_open` field in the `Shop` model accordingly.
- The scheduler will be configured to run this job every 5-10 minutes.

### Step 3: Add Manual Override
- Add a new boolean field to the `Shop` model called `manual_override` (default `False`).
- In the `edit_shop` view, when a seller manually toggles the `is_open` status, set `manual_override` to `True`.
- The `update_shop_statuses` job will skip any shop where `manual_override` is `True`.
- Add a button in the "Edit Shop" template to "Resume Automated Schedule", which sets `manual_override` back to `False`.

## 2. Seller Responses to Reviews

This feature will allow sellers to write a public response to reviews left on their shop.

### Step 1: Create a ReviewResponse Model
- In `models.py`, create a new `ReviewResponse` model:
  ```python
  class ReviewResponse(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      response_text = db.Column(db.Text, nullable=False)
      created_at = db.Column(db.DateTime, default=datetime.utcnow)
      review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False, unique=True)
      review = db.relationship('Review', backref=db.backref('response', uselist=False))
  ```
- Run `flask db migrate` and `flask db upgrade` to apply the changes.

### Step 2: Create a Response Form
- In `forms.py`, create a `ReviewResponseForm`:
  ```python
  class ReviewResponseForm(FlaskForm):
      response_text = TextAreaField('Your Response', validators=[DataRequired(), Length(max=500)])
  ```

### Step 3: Create a Route for Adding Responses
- In `routes/shop.py`, create a new route `/review/<int:review_id>/respond`.
- This route will be `@login_required` and will check that `current_user` is the owner of the shop associated with the review.
- It will process the `ReviewResponseForm` and create a new `ReviewResponse` object linked to the review.

### Step 4: Update Templates
- In `templates/shop.html`, modify the review loop:
    - If a review has a response (`review.response`), display it underneath the review.
    - If the current user is the shop owner and a review does *not* have a response, display a "Respond" button that links to the new response route.

## 3. Advanced Search and Filtering

This feature will implement the missing filtering logic for the search page.

### Step 1: Update the Search Route
- In `routes/main.py`, modify the `/search` route to handle the additional filters.
- The query will need to be built dynamically based on the form data.

### Step 2: Implement Rating Filter
- If `form.min_rating.data` is present:
    - Add a filter to the `Shop` query: `query = query.filter(Shop.average_rating >= float(form.min_rating.data))`
    - Note: The `average_rating` property in the `Shop` model will work for this, but for better performance on large datasets, this could be converted to a real database column that is updated via a trigger or on review submission. For now, the property is sufficient.

### Step 3: Implement Distance Filter
- This is the most complex part.
- If `form.max_distance.data` is present:
    1. Get the user's location. This will require asking for their location on the search page or having them enter an address which is then geocoded. A `user_lat` and `user_lon` will be needed.
    2. The current query fetches all shops and then filters them in Python. This is inefficient. A better approach is to perform a bounding box query first to limit the results from the database.
    3. A simpler, less performant approach (acceptable for a small number of shops) is to:
        - Fetch all shops that match the other criteria (name, category).
        - Iterate through the results in Python.
        - Use the `location_service.calculate_distance` function to calculate the distance between the user and each shop.
        - Keep only the shops that are within `form.max_distance.data`.
- The `location_service` already has a `get_nearby_shops` function that can be adapted for this purpose.

### Step 4: Update the Search Template
- In `templates/search.html`, ensure the form correctly displays the selected filter values after submission.
- Add a mechanism to get the user's location if they want to filter by distance (e.g., a "Use My Location" button that uses JavaScript's Geolocation API).
