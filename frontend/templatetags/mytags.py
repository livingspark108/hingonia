import re
from urllib.parse import urlparse, parse_qs

from django.db.models import Sum
from urllib.parse import urlencode
from django.conf import settings

from django import template
from django.urls import reverse, NoReverseMatch
import json
import pytz
from datetime import date
from django.utils import timezone
import dateutil.parser
import random
from django.utils.html import mark_safe


from apps.front_app.models import Campaign, Setting, UploadedFile, HomeSlider, HomePageContent
from apps.user.models import TransactionDetails, ProductItemTrans

utc=pytz.UTC
from datetime import datetime

register = template.Library()

@register.filter(name='convert_spaces_to_span')
def convert_spaces_to_span(value):
    return re.sub(r"'(.*?)'", r'<span>\1</span>', value)

@register.simple_tag()
def generate_random_color():
    # Define the list of colors
    colors = ['#00C4AC', '#C21959', '#FF7A41']

    # Randomly choose one of the colors
    return random.choice(colors)

@register.simple_tag()
def get_campain_data():
    return Campaign.objects.all()

@register.simple_tag()
def get_setting_data():
    return Setting.objects.first()


@register.simple_tag()
def get_home_setting_data():
    return HomePageContent.objects.first()


@register.simple_tag()
def calculate_support_amt(amt):
    try:
        amt = float(amt)  # Convert to float for better precision
        amt_1 = (8 / 100) * amt
        amt_2 = (12 / 100) * amt
        amt_3 = (14 / 100) * amt
        amt_4 = (16 / 100) * amt
    except (ValueError, ZeroDivisionError):
        return 0, 0, 0, 0  # Return default values if input is invalid or zero

    return int(amt_1), int(amt_2), int(amt_3), int(amt_4)

@register.simple_tag()
def get_minimum_value():
    setting_obj = Setting.objects.first()
    if setting_obj.min_order_value:
        return setting_obj.min_order_value
    else:
        return 250
@register.filter(name='handle_none')
def handle_none(num):
    if not num:
        return ""
    else:
        return num

@register.filter(name='handle_zero')
def handle_zero(num):
    if not num:
        return 0
    else:
        return num


@register.filter(name='add_spam_tag')
def add_spam_tag(value):
    try:
        words = value.split()
        last_word = words[-1]
        modified_string = ' '.join(words[:-1]) + f' <span class="color-2">{last_word}</span>'
        return modified_string
    except:
        return ""

@register.simple_tag()
def calculate_percentage(target, achieved):
    try:
        if target == 0:
            return 0  # Avoid division by zero
        percentage_achieved = int((achieved / target) * 100)

        return percentage_achieved
    except:
        return 0


@register.simple_tag()
def divide(value, arg):
    if value and arg:
        try:
            return round(value / arg)
        except (ValueError, ZeroDivisionError):
            return None
    else:
        return None


@register.simple_tag()
def get_campaign_data(campaign_id):
    print(campaign_id)
    campaign_obj = Campaign.objects.filter(id=campaign_id).first()
    if campaign_obj:
        tran_count = TransactionDetails.objects.filter(campaign_id=campaign_id)
        if tran_count:
            total_sum = sum(item.amount for item in tran_count)
        else:
            total_sum = 0
        pr = calculate_percentage(campaign_obj.goal,total_sum)
        if campaign_obj.youtube_link:
            try:
                video_id = get_youtube_embed(campaign_obj.youtube_link)
            except:
                video_id = ""

        else:
            video_id = ""


        context = {
            'campaign_obj':campaign_obj,
            'target': total_sum,
            'percent': pr,
            'video_id':video_id,
            'date': datetime.now()
        }
        return context
    else:
        return False

@register.simple_tag()
def generate_price(price):
    context = {
        'one': price,
        'two': price * 2,
        'three': price * 3
    }
    return context

@register.simple_tag()
def generate_tag(data):
    if data:
        basis_string = data

        basis_list = basis_string.split()

        tag_classes = ["badge bg-danger", "badge bg-warning",
                       "badge bg-success"]

        random_tags = []

        for basis in basis_list:
            tag_class = random.choice(tag_classes)
            random_tag = f'<span style="margin-left: 5px;padding: 10px;" class="{tag_class}">{basis}</span>'
            random_tags.append(random_tag)

        tag_html = ""
        # Print random tags
        for tag in random_tags:
            tag_html += tag


        return tag_html
    else:
        return ""

@register.simple_tag()
def get_cam_item(product_id,camp_id):

    order_ids = TransactionDetails.objects.filter(campaign_id=camp_id).values_list('order_id', flat=True)
    # Get the sum of the quantity field from ProductItemTrans for the filtered order IDs
    quantity_sum = ProductItemTrans.objects.filter(order_id__in=order_ids, product_id=product_id).aggregate(
        total_quantity=Sum('quantity'))

    # Access the sum value
    total_quantity = quantity_sum['total_quantity']
    if not total_quantity:
        total_quantity = 0
    context = {
        'total_quantity':total_quantity
    }
    return context


@register.simple_tag()
def get_cam_product_item(order_id):


    quantity_sum = ProductItemTrans.objects.filter(order_id=order_id)

    return quantity_sum


@register.simple_tag()
def get_gallery(id,type):
    upload_obj = UploadedFile.objects.filter(uploader_id=id,file_type=type).order_by('-uploaded_at')
    if upload_obj:
        return upload_obj
    else:
        return ""


@register.simple_tag()
def get_slider():
    upload_obj = HomeSlider.objects.all()
    if upload_obj:
        return upload_obj
    else:
        return ""


@register.filter(name='handle_image_url')
def handle_image_url(img):
    if img:
        return img.url
    else:
        return "/static/frontend/assets/images/place-holder.png"

@register.simple_tag()
def get_youtube_embed(link):
    # Extract the video ID from the URL
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', link)
    if video_id_match:
        video_id = video_id_match.group(1)
        # Generate the embed URL
        embed_url = f'https://www.youtube.com/embed/{video_id}'
        return embed_url
    return ''

@register.filter(name='generate_tag')
def generate_tag(txt):
    if txt:
        words = txt.split()  # Split the text by spaces
        return ' '.join([f"#{word}" for word in words])  # Prefix each word with '#'
    else:
        return txt

@register.simple_tag()
def get_youtube_embed(link):
    # Extract the video ID from the URL
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', link)
    if video_id_match:
        video_id = video_id_match.group(1)
        # Generate the embed URL
        embed_url = f'https://www.youtube.com/embed/{video_id}'
        return embed_url
    return ''


@register.filter
def indian_number_format(value):
    if not value:
        return "0"
    try:
        value = int(value)
        # Convert number to string for easier manipulation
        value_str = str(value)
        # Split the string into two parts: before and after the last 3 digits
        if len(value_str) > 3:
            last_three = value_str[-3:]
            remaining = value_str[:-3]
            # Reverse the remaining part and insert commas every 2 digits
            remaining = remaining[::-1]
            chunks = [remaining[i:i + 2] for i in range(0, len(remaining), 2)]
            # Reverse the chunks back and join them with commas
            remaining_with_commas = ','.join(chunks)[::-1]
            # Combine the parts and return the result
            return remaining_with_commas + ',' + last_three
        else:
            return value_str
    except (ValueError, TypeError):
        return value



@register.filter(name='is_image')
def is_image(file_url):
    """Check if a file URL is an image based on its extension."""
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    return any(file_url.lower().endswith(ext) for ext in valid_extensions)


@register.simple_tag
def share_icons_images(slug, text=None):
    # Construct URL to be shared
    url = settings.BASE_URL + "/ongoing-devotion/" + slug

    platforms = {
        "whatsapp": {
            "base_url": "https://api.whatsapp.com/send",
            "img_src": "/static/frontend/assets/images/campaign/wp.svg",
        },
        "facebook": {
            "base_url": "https://www.facebook.com/sharer/sharer.php",
            "img_src": "/static/frontend/assets/images/campaign/facebook.svg",
        },

    }

    share_html = ""

    # Generate share icons for each platform
    for platform, data in platforms.items():
        base_url = data["base_url"]
        img_src = data["img_src"]

        if not base_url:  # Instagram doesn't support direct share link, fallback to a profile
            share_html += f'<a href="{url}" target="_blank"><img src="{img_src}" class="img-fluid" alt="{platform}"></a>'
        else:
            query_params = {"url": url}
            if text:
                query_params["text"] = text

            share_url = f"{base_url}?{urlencode(query_params)}"
            share_html += f'<a href="{share_url}" target="_blank"><img src="{img_src}" class="img-fluid" alt="{platform}"></a>'

    # Mark the generated HTML as safe for rendering
    return mark_safe(share_html)

@register.simple_tag
def share_icons(slug, text=None):
    # Base URL for the site
    url = settings.BASE_URL + "/ongoing-devotion/" + slug

    """
    Generates social media share icons based on the given URL.

    :param url: The URL to be shared.
    :param text: Optional text to be included with the share link.
    :return: HTML for social media share icons.
    """
    platforms = {
        "whatsapp": {
            "base_url": "https://api.whatsapp.com/send",
            "icon_class": "bi bi-whatsapp wp_color",
        },
        "facebook": {
            "base_url": "https://www.facebook.com/sharer/sharer.php",
            "icon_class": "bi bi-facebook fb_color",
        },
        "linkedin": {
            "base_url": "https://www.linkedin.com/shareArticle",
            "icon_class": "bi bi-linkedin linkedin_color",
        },
    }

    share_html = ""

    # Generate share icons for each platform
    for platform, data in platforms.items():
        base_url = data["base_url"]
        icon_class = data["icon_class"]

        if not base_url:  # Instagram does not support direct share link
            # Instagram sharing can be linked to a profile or a fallback option
            share_html += f'<a href="{url}" target="_blank"><i class="{icon_class}"></i></a>'
        else:
            query_params = {"url": url}
            if text:
                query_params["text"] = text  # Add text to the share URL if provided

            # Build the full share URL with query params
            share_url = f"{base_url}?{urlencode(query_params)}"
            share_html += f'<a href="{share_url}" target="_blank"><i class="{icon_class}"></i></a>'

    return mark_safe(share_html)