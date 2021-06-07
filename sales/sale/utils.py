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


def get_key(res_by):
    if res_by=="#1":
        return "transaction_id"
    elif res_by=="#2":
        return "created"


def get_chart(chart_type, data, result_by, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10, 4))
    key = get_key(result_by)
    d = data.groupby(key, as_index=False)['total_price'].agg(sum)
    if chart_type=="#1":
        print("Bar chart")
        # plt.bar(d['transaction_id'], d['total_price'])
        sns.barplot(x=key, y='total_price', data=d)
    elif chart_type=="#2":
        print("Pie chart")
        label = d[key].values
        plt.pie(data = d[[key, 'total_price']], x='total_price', labels=label)
    elif chart_type=="#3":
        print("Line chart")
        plt.plot(d[key],d['total_price'], marker='o', color='green', linestyle='--')
    else : 
        print("Invalid chart type")
    plt.tight_layout()
    chart = get_graph()
    return chart