from application.models  import *
from application.permissions import *
from fpdf import FPDF
from datetime import datetime
from sqlalchemy import func
from datetime import datetime, timedelta
from flask import jsonify
import csv
import os
from application import app

# Report for daily purchases

from flask_jwt_extended import jwt_required
from application.models import *
from application.permissions import *
from fpdf import FPDF
from datetime import datetime, timedelta  # Make sure to import datetime
from flask import jsonify, request
import csv
import os

# Report for daily purchases

def daily_purchase_report(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d')
    start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + timedelta(days=1)

    daily_purchases = Purchase.query.filter(
        Purchase.purchase_date >= start_date,
        Purchase.purchase_date < end_date
    ).all()

    return daily_purchases

# Report for monthly purchases


# Report for monthly purchases

def monthly_purchase_report(month, year):
    start_date = datetime(year, month, 1)
    end_date = start_date.replace(month=start_date.month + 1) if start_date.month < 12 else start_date.replace(year=start_date.year + 1, month=1)

    monthly_purchases = Purchase.query.filter(
        Purchase.purchase_date >= start_date,
        Purchase.purchase_date < end_date
    ).all()

    return monthly_purchases


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        header_text = 'Daily Purchase Report - ' + str(datetime.utcnow().date())
        self.cell(0, 10, header_text, 0, 1, 'C')


    def chapter_title(self, num, label):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Item {}: {}'.format(num, label), 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

# Function to generate and save daily purchase report in PDF format using FPDF

def save_daily_purchase_pdf_fpdf(purchases, filename):
    pdf = PDF()
    pdf.add_page()

    for i, purchase in enumerate(purchases, 1):
        pdf.chapter_title(i, purchase.item_name)
        pdf.chapter_body(f"Quantity: {purchase.item_quantity}\nTotal Amount: {purchase.total_amount}")

    pdf.output(filename)
    try:
        # Save daily purchase report in PDF using FPDF
        daily_purchases = daily_purchase_report(datetime.utcnow())
        save_daily_purchase_pdf_fpdf(daily_purchases, 'daily_purchase_report_fpdf.pdf')

        return jsonify({'message': 'Items purchased successfully'}), 200  # OK
    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred while processing the purchase'}), 500




# Function to generate and save daily purchase report in CSV format

def save_daily_purchase_csv(purchases, filename):
    fieldnames = ['Item Name', 'Quantity', 'Total Amount']

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for purchase in purchases:
            writer.writerow({
                'Item Name': purchase.item_name,
                'Quantity': purchase.item_quantity,
                'Total Amount': purchase.total_amount
            })

# Function to generate and save monthly purchase report in CSV format

def save_monthly_purchase_csv(purchases, filename):
    fieldnames = ['Item Name', 'Quantity', 'Total Amount']

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for purchase in purchases:
            writer.writerow({
                'Item Name': purchase.item_name,
                'Quantity': purchase.item_quantity,
                'Total Amount': purchase.total_amount
            })



import matplotlib.pyplot as plt

# Function to generate and save a bar chart for daily purchase report
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import io
import base64

def generate_daily_purchase_bar_chart(purchases):
    items = [purchase.item_name for purchase in purchases]
    quantities = [purchase.item_quantity for purchase in purchases]

    plt.bar(items, quantities)
    plt.xlabel('Item Name')
    plt.ylabel('Quantity')
    plt.title('Daily Purchase Report')
    plt.xticks(rotation=45, ha='right')

    # Save the figure to a BytesIO object
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert the figure to base64
    image_base64 = base64.b64encode(buffer.read()).decode()

    # Close the figure
    plt.close()

    return image_base64

def generate_monthly_purchase_bar_chart(purchases):
    items = [purchase.item_name for purchase in purchases]
    quantities = [purchase.item_quantity for purchase in purchases]

    plt.bar(items, quantities)
    plt.xlabel('Item Name')
    plt.ylabel('Quantity')
    plt.title('Monthly Purchase Report')
    plt.xticks(rotation=45, ha='right')

    # Save the figure to a BytesIO object
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert the figure to base64
    image_base64 = base64.b64encode(buffer.read()).decode()

    # Close the figure
    plt.close()

    return image_base64