import base64
import uuid
from customers.models import Customer
from profiles.models import Profile
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import seaborn as sns

def generate_code() :
    code = str(uuid.uuid4()).replace('-', '')[:12]
    return code


def get_salesman_from_id(id):
    salesman = Profile.objects.get(id=id)
    return salesman


def get_customer_from_id(id):
    customer = Customer.objects.get(id=id)
    return customer


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_chart(chart_type, data, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10, 4))
    if chart_type=="#1":
        print("Bar chart")
        # plt.bar(data['transaction_id'], data['total_price'])
        sns.barplot(x='transaction_id', y='total_price', data=data)
    elif chart_type=="#2":
        print("Pie chart")
        label = kwargs.get('labels')
        plt.pie(data = data[['transaction_id', 'total_price']], x='total_price', labels=label)
    elif chart_type=="#3":
        print("Line chart")
        plt.plot(data['transaction_id'],data['total_price'], marker='o', color='green', linestyle='--')
    else : 
        print("Invalid chart type")
    plt.tight_layout()
    chart = get_graph()
    return chart