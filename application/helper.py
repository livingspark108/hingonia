from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
import threading
from xlrd import open_workbook
import csv
import razorpay as razorpay

from application.email_helper import send_email_background
from apps.user.models import SubscriptionPlan


def convert_file_to_dict(file):
    if file.name.endswith('.csv'):
        fstring = file.read().decode('UTF-8')
        students_dicts = [{k: v for k, v in row.items()} for row in
                          csv.DictReader(fstring.splitlines(), skipinitialspace=True)]
        print(students_dicts)
        return students_dicts, False
    elif file.name.endswith('.xls') or file.name.endswith('.xlsx'):
        wb = open_workbook(file_contents=file.read())
        values = []
        for s in wb.sheets():
            for row in range(1, s.nrows):
                col_names = s.row(0)
                col_value = {}
                for name, col in zip(col_names, range(s.ncols)):
                    value = (s.cell(row, col).value)
                    nkey = name.value
                    if nkey != '':
                        col_value[nkey] = value
                new = {k: col_value[k] for k in col_value if col_value[k]}
                if new != {}:
                    values.append(col_value)
        print(values)
        return values, False
    else:
        return 'Please select valid CSV or Excel file', False


def send_password_set_email(user, request):
    reset_form = PasswordResetForm({'email': user.email})
    assert reset_form.is_valid()
    reset_form.save(
        request=request,
        use_https=request.is_secure(),
        subject_template_name='frontend/registration/account_creation_subject.txt',
        email_template_name='frontend/registration/account_creation_email.html',
    )


class EmailThread(threading.Thread):
    def __init__(self, user, request):
        self.user = user
        self.request = request
        threading.Thread.__init__(self)

    def run(self):
        if self.user.type == 'student':
            template_name = 'frontend/registration/account_creation_email.html'
        else:
            template_name = 'frontend/registration/teacher_account_creation_email.html'
        reset_form = PasswordResetForm({'email': self.user.email})
        assert reset_form.is_valid()
        reset_form.save(
            request=self.request,
            use_https=self.request.is_secure(),
            subject_template_name='frontend/registration/account_creation_subject.txt',
            email_template_name=template_name,
            html_email_template_name=template_name,
        )


def send_password_set_email_background(user, request):
    EmailThread(user, request).start()


def get_full_name(user):
    if user.type == 'student':
        return user.student_profile
    else:
        return user.teacher_profile


def send_newsletter(request, to, context={}):
    template = 'email/newsletter_mail_template.html'
    for reciepint in to:
        send_email_background(request, reciepint, template, context, subject='Newsletter From Alternates')

def send_contact_us(request, to, context={}):
    template = 'frontend/email/contact_us_template.html'
    for reciepint in to:
        send_email_background(request, reciepint, template, context, subject='Contact Us - Confirmation')


def get_stripe_public_key():
    return settings.STRIPE_LIVE_PUBLIC_KEY if settings.STRIPE_LIVE_MODE else settings.STRIPE_LIVE_PUBLIC_KEY

def get_stripe_secret_key():
    return settings.STRIPE_LIVE_SECRET_KEY if settings.STRIPE_LIVE_MODE else settings.STRIPE_TEST_SECRET_KEY



def fetch_and_save_plans_from_razorpay():
    # Initialize Razorpay client
    razorpay_client = razorpay.Client(auth=(settings.RAZOR_PAY_ID, settings.RAZOR_PAY_SECRET))

    try:
        # Fetch all plans from Razorpay
        plans = razorpay_client.plan.all()
        print(plans)
        for plan_data in plans['items']:
            # Check if the plan already exists in the database
            plan, created = SubscriptionPlan.objects.update_or_create(
                plan_id=plan_data['id'],
                defaults={
                    'name': plan_data['item']['name'],
                    'description': plan_data['item']['description'],
                    'price': plan_data['item']['amount'] / 100,  # Amount is in paise
                }
            )

            if created:
                print(f"Created new plan: {plan.name}")
            else:
                print(f"Updated existing plan: {plan.name}")

    except Exception as e:
        print(f"Error fetching plans from Razorpay: {str(e)}")