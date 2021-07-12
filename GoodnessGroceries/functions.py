from .models import ProductReviews


def handle_product_reviews(prod_reviews):
    # Main and Secondary Indicator
    main_indicators = []
    secondary_indicators = []

    for prod_review in prod_reviews:
        main_indicators.append(prod_review.selected_indicator_main_id)
        secondary_indicators.append(
            prod_review.selected_indicator_secondary_id)

    number_of_main_indicators = dict()
    for indicator in main_indicators:
        number_of_main_indicators[indicator] = prod_reviews.filter(
            selected_indicator_main_id=indicator).count()

    number_of_secondary_indicators = dict()
    for indicator in secondary_indicators:
        number_of_secondary_indicators[indicator] = prod_reviews.filter(
            selected_indicator_secondary_id=indicator).count()

    # Price Checkbox Selected
    number_of_price_checkbox_selected = dict()
    number_of_price_checkbox_selected["True"] = prod_reviews.filter(
        price_checkbox_selected=True).count()
    number_of_price_checkbox_selected["False"] = prod_reviews.filter(
        price_checkbox_selected=False).count()

    # Number of product reviews per day for past 10 days
    timestamps = []
    recent_prod_review_of_last_10_days = ProductReviews.objects.order_by(
        '-timestamp')
    for prod_review in recent_prod_review_of_last_10_days:
        if prod_review.timestamp.date() not in timestamps:
            timestamps.append(prod_review.timestamp.date())

    number_of_prod_reviews_per_day = dict()

    for date in timestamps[:10]:
        number_of_prod_reviews_per_day[date] = 0
        for prod_review in prod_reviews:
            if prod_review.timestamp.date() == date:
                number_of_prod_reviews_per_day[date] += 1

    return number_of_main_indicators, number_of_secondary_indicators, number_of_price_checkbox_selected, number_of_prod_reviews_per_day
