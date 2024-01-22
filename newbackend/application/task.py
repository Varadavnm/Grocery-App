from application import celery, mail, app
from flask_mail import Message
from celery import shared_task
from datetime import datetime, timedelta
from fpdf import FPDF
from application.models import Purchase, Product, User
import tempfile
import logging

@celery.task
def send_daily_purchase_report():
    with app.app_context():
        try:
            today = datetime.utcnow().date()
            purchases_today = Purchase.query.filter(
                Purchase.purchase_date >= today,
                Purchase.purchase_date < today + timedelta(days=1)
            ).all()
            if not purchases_today:
                send_no_purchase_notification()
                return "No purchases today. Notification email sent."

            pdf_path = generate_purchase_report_pdf(purchases_today)
            users = User.query.all()
            recipients = []
            for user in users:
                if "admin" in user.roles:
                    recipients.append(user.email)
            msg = Message("Daily Purchase Report", sender="zoe.smith12233@gmail.com", recipients=recipients)
            msg.body = "Please find the attached daily purchase report."

            with open(pdf_path, 'rb') as pdf_file:
                msg.attach("daily_purchase_report.pdf", "application/pdf", pdf_file.read())

            mail.send(msg)

            return "Email sent successfully!"

        except Exception as e:
            logging.exception(f"An error occurred: {e}")
            print(e)
            return f"Error occurred during task execution: {str(e)}"

@celery.task
def send_no_purchase_notification():
    with app.app_context():
        try:
            users = User.query.all()
            recipients = []
            for user in users:
                if "admin" in user.roles:
                    recipients.append(user.email)
            msg = Message("No Purchase Today", sender="zoe.smith12233@gmail.com", recipients=recipients)
            msg.body = "No purchases were made today."

            mail.send(msg)

            return "Notification email sent successfully!"

        except Exception as e:
            logging.exception(f"An error occurred: {e}")
            return "Error occurred during task execution."

@celery.task
def generate_purchase_report_pdf(purchases):
    with app.app_context():
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Daily Purchase Report - {datetime.utcnow().date()}", ln=True, align='C')

            for purchase in purchases:
                pdf.cell(200, 10, txt=f"{purchase.item_name} - {purchase.item_quantity} - {purchase.total_amount}", ln=True, align='L')

            _, pdf_path = tempfile.mkstemp(suffix=".pdf")
            pdf.output(pdf_path)

            return pdf_path

        except Exception as e:
            logging.exception(f"An error occurred: {e}")
            return None

@celery.task
def check_product_stock():
    with app.app_context():
        try:
            products = Product.query.all()
            for product in products:
                if product.stock == 0:
                    message = Message()
                    message.subject = "Out of stock!"
                    message.body = f'The {product.name} is out of stock'
                    users = User.query.all()
                    recipients = []
                    for user in users:
                        if "admin" in user.roles or "manager" in user.roles:
                            recipients.append(user.email)
                    message.recipients = recipients
                    mail.send(message)

            return "Checked product stock successfully!"

        except Exception as e:
            logging.exception(f"An error occurred: {e}")
            return "Error occurred during task execution."

@celery.task
def send_login_confirmation(user_id):
    with app.app_context():
        try:
            curr_user = User.query.filter_by(id=user_id).first()
            print(curr_user)
            message = Message()
            message.subject = "Welcome to Grocery-store"
            message.body = "You are successfully logged into the Grocery_store,!"
            user_email = curr_user.email
            message.recipients = [user_email]
            mail.send(message)

            return "Login confirmation email sent successfully!"

        except Exception as e:
            logging.exception(f"An error occurred: {e}")
            return "Error occurred during task execution."
@celery.task
def send_approval_email(email):
    with app.app_context():
        print(email)
        msg = Message(
            subject="Manager Approval",
            recipients=[email],
            body="Congratulations! You have been approved as a manager. You can now log in as a manager. All the best!"
        )
        mail.send(msg)

# tasks.py



@celery.task
def send_monthly_purchase_report_email():
    from application.report import monthly_purchase_report, save_monthly_purchase_csv
    try:
        current_month = app.config['CURRENT_MONTH']
        current_year = app.config['CURRENT_YEAR']
        # Generate the monthly purchase report
        monthly_purchases = monthly_purchase_report(current_month, current_year)
        # Save monthly purchase report in CSV
        filename = 'monthly_purchase.csv'
        save_monthly_purchase_csv(monthly_purchases, filename)
        subject = 'Monthly Purchase Report'
        body = f'This is the purchase report for the {current_month}. Please find the attached report.'
        from application.models import User, roles_users
        users = User.query.all()
        recipients = []
        for user in users:
            if "admin" in user.roles:
                recipients.append(user.email)
        with app.open_resource(filename) as attachment:
            message = Message(subject=subject, body=body, recipients=recipients)
            message.attach(filename, 'text/csv', attachment.read())
        # Send the email
        mail.send(message)

        return f'Monthly purchase report for {current_month} {current_year} sent successfully'
    except Exception as e:
        print(e)
        return 'An error occurred while sending the monthly purchase report'

@celery.task
def send_inactive_customer_remainder():
    with app.app_context():
        users = User.query.all()
        customers = []
        for user in users:
            if "customer" in user.roles and customer.last_login_time:
                last_login_time_str = user.last_login
                last_login_time = datetime.strptime(last_login_time_str, "%Y-%m-%d %H:%M:%S.%f")
                time_difference = datetime.utcnow()-last_login_time
                if time_difference > timedelta(hours=24):
                    customers.append(user.email)
        if len(customers)>0:
            for customer in customers:
                
                subject = f'{customer.username} you were not active for one day'
                body = "Explore latest products in our store"
                message = Message(subject=subject, body = body, sender="zoe.smith12233@gmail.com", recipients=[customer])
                return "message sent successfully"
    return "Something went wrong"
