from flask import Flask, request, redirect, render_template_string, flash

app = Flask(__name__)
app.secret_key = "swe40006-task4-secret"


# ---------------------------------------------------------
# Sample expense data
# ---------------------------------------------------------
expenses = [
    {"id": 1, "description": "Lunch", "amount": 15.50, "category": "Food"},
    {"id": 2, "description": "Grab", "amount": 25.00, "category": "Transport"},
    {"id": 3, "description": "Textbook", "amount": 105.00, "category": "Education"},
]


# Category icons
category_icons = {
    "Food": "🍔",
    "Transport": "🚗",
    "Education": "📚",
    "Shopping": "🛍️",
    "Bills": "💡",
    "Entertainment": "🎬",
    "Health": "🏥",
    "Other": "📦",
}


# ---------------------------------------------------------
# HTML + CSS
# ---------------------------------------------------------
HTML = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>SWE40006 Expense Tracker</title>

    <style>

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, Helvetica, sans-serif;
            background: #f7f6fc;
            color: #25243a;
            min-height: 100vh;
        }


        /* -------------------------------------------------
           Header
        ------------------------------------------------- */

        header {
            background: linear-gradient(135deg, #4f46a5, #7c3aed);
            color: white;
            padding: 42px 20px;
            text-align: center;
        }

        header h1 {
            font-size: 38px;
            margin-bottom: 8px;
        }

        header p {
            opacity: 0.92;
            margin-top: 6px;
            font-size: 16px;
        }


        /* -------------------------------------------------
           Main container
        ------------------------------------------------- */

        .container {
            max-width: 1050px;
            margin: 35px auto;
            padding: 0 20px 40px;
        }


        /* -------------------------------------------------
           Notification
        ------------------------------------------------- */

        .notification {
            padding: 15px 18px;
            margin-bottom: 20px;
            border-radius: 10px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: opacity 0.4s ease;
        }

        .notification.success {
            background: #ecfdf3;
            color: #18794e;
            border: 1px solid #b7ebcc;
        }

        .notification.deleted {
            background: #fff1f2;
            color: #b42318;
            border: 1px solid #fecdd3;
        }


        /* -------------------------------------------------
           Summary
        ------------------------------------------------- */

        .summary {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 25px;
        }

        .summary-card {
            background: white;
            padding: 25px;
            border-radius: 16px;
            box-shadow: 0 5px 18px rgba(65, 55, 120, 0.08);
            border: 1px solid #ebe9f5;
        }

        .summary-card .icon {
            font-size: 26px;
            margin-bottom: 10px;
        }

        .summary-card small {
            color: #77738d;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .summary-card h2 {
            color: #5b4bb7;
            margin-top: 8px;
            font-size: 28px;
        }


        /* -------------------------------------------------
           Cards
        ------------------------------------------------- */

        .card {
            background: white;
            border-radius: 16px;
            padding: 28px;
            margin-bottom: 25px;
            box-shadow: 0 5px 18px rgba(65, 55, 120, 0.08);
            border: 1px solid #ebe9f5;
        }

        .card h2 {
            margin-bottom: 22px;
            font-size: 24px;
        }


        /* -------------------------------------------------
           Expense form
        ------------------------------------------------- */

        .expense-form {
            display: grid;
            grid-template-columns: 2fr 1.2fr 1.2fr auto;
            gap: 12px;
            align-items: start;
        }

        .field-group {
            display: flex;
            flex-direction: column;
        }

        input,
        select {
            width: 100%;
            padding: 14px;
            border: 1px solid #d9d5e7;
            border-radius: 10px;
            font-size: 15px;
            outline: none;
            background: white;
            height: 48px;
        }

        input:focus,
        select:focus {
            border-color: #7c3aed;
            box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.10);
        }

        input.input-error {
            border-color: #e5484d;
            background: #fffafa;
        }

        input.input-error:focus {
            border-color: #e5484d;
            box-shadow: 0 0 0 3px rgba(229, 72, 77, 0.10);
        }


        /* Inline validation */

        .field-error {
            color: #c83232;
            font-size: 13px;
            font-weight: 600;
            margin-top: 7px;
            padding-left: 3px;
        }


        /* Add button */

        .add-button {
            border: none;
            background: #6554c0;
            color: white;
            padding: 14px 22px;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            font-size: 15px;
            transition: 0.2s;
            height: 48px;
            white-space: nowrap;
        }

        .add-button:hover {
            background: #5143a5;
            transform: translateY(-1px);
        }


        /* -------------------------------------------------
           Expense table
        ------------------------------------------------- */

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th {
            text-align: left;
            padding: 15px;
            background: #f3f1fa;
            color: #565169;
            font-size: 14px;
        }

        td {
            padding: 16px 15px;
            border-bottom: 1px solid #efedf5;
        }

        .category {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            background: #f1effb;
            color: #574a9f;
            padding: 7px 11px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
        }

        .amount {
            font-weight: bold;
            color: #4f46a5;
        }


        /* Delete button */

        .delete-button {
            border: none;
            background: #fff0f0;
            color: #c83232;
            padding: 9px 14px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            transition: 0.2s;
        }

        .delete-button:hover {
            background: #c83232;
            color: white;
        }


        /* -------------------------------------------------
           Empty state
        ------------------------------------------------- */

        .empty-state {
            text-align: center;
            padding: 45px 20px;
            color: #77738d;
        }

        .empty-state .emoji {
            font-size: 45px;
            margin-bottom: 12px;
        }


        /* -------------------------------------------------
           Docker status
        ------------------------------------------------- */

        .docker-status {
            margin-top: 20px;
            padding: 13px;
            text-align: center;
            background: #f0fdf4;
            color: #16803d;
            border: 1px solid #bbf7d0;
            border-radius: 10px;
            font-weight: bold;
        }


        /* -------------------------------------------------
           Footer
        ------------------------------------------------- */

        footer {
            text-align: center;
            color: #77738d;
            margin-top: 30px;
            line-height: 1.8;
            font-size: 14px;
        }


        /* -------------------------------------------------
           Responsive design
        ------------------------------------------------- */

        @media (max-width: 800px) {

            .summary {
                grid-template-columns: 1fr;
            }

            .expense-form {
                grid-template-columns: 1fr;
            }

            table {
                font-size: 13px;
            }

            th,
            td {
                padding: 11px 7px;
            }

            header h1 {
                font-size: 30px;
            }

        }

    </style>

</head>


<body>


<header>

    <h1>💰 Expense Tracker</h1>

    <p>SWE40006 - Software Deployment and Evolution</p>

    <p>Task 4.3 - Docker Web Application</p>

</header>


<div class="container">


    <!-- -------------------------------------------------
         Add/Delete notifications
    -------------------------------------------------- -->

    {% with messages = get_flashed_messages(with_categories=true) %}

        {% if messages %}

            {% for category, message in messages %}

                {% if category == "success" %}

                    <div class="notification success auto-hide">
                        ✓ {{ message }}
                    </div>

                {% elif category == "deleted" %}

                    <div class="notification deleted auto-hide">
                        🗑️ {{ message }}
                    </div>

                {% endif %}

            {% endfor %}

        {% endif %}

    {% endwith %}



    <!-- -------------------------------------------------
         Summary cards
    -------------------------------------------------- -->

    <div class="summary">


        <div class="summary-card">

            <div class="icon">💵</div>

            <small>Total Expenses</small>

            <h2>RM {{ "%.2f"|format(total) }}</h2>

        </div>


        <div class="summary-card">

            <div class="icon">🧾</div>

            <small>Number of Expenses</small>

            <h2>{{ expenses|length }}</h2>

        </div>


    </div>



    <!-- -------------------------------------------------
         Add expense
    -------------------------------------------------- -->

    <div class="card">

        <h2>➕ Add New Expense</h2>


        <form
            class="expense-form"
            method="POST"
            action="/add"
            novalidate
        >


            <!-- Description -->

            <div class="field-group">

                <input
                    type="text"
                    name="description"
                    placeholder="Expense description"
                    value="{{ form_description }}"
                    class="{% if description_error %}input-error{% endif %}"
                >

                {% if description_error %}

                    <div class="field-error">
                        ⚠️ {{ description_error }}
                    </div>

                {% endif %}

            </div>



            <!-- Amount -->

            <div class="field-group">

                <input
                    type="text"
                    name="amount"
                    placeholder="Amount (RM)"
                    value="{{ form_amount }}"
                    class="{% if amount_error %}input-error{% endif %}"
                >

                {% if amount_error %}

                    <div class="field-error">
                        ⚠️ {{ amount_error }}
                    </div>

                {% endif %}

            </div>



            <!-- Category -->

            <div class="field-group">

                <select name="category">

                    <option
                        value="Food"
                        {% if form_category == "Food" %}selected{% endif %}
                    >
                        🍔 Food
                    </option>

                    <option
                        value="Transport"
                        {% if form_category == "Transport" %}selected{% endif %}
                    >
                        🚗 Transport
                    </option>

                    <option
                        value="Education"
                        {% if form_category == "Education" %}selected{% endif %}
                    >
                        📚 Education
                    </option>

                    <option
                        value="Shopping"
                        {% if form_category == "Shopping" %}selected{% endif %}
                    >
                        🛍️ Shopping
                    </option>

                    <option
                        value="Bills"
                        {% if form_category == "Bills" %}selected{% endif %}
                    >
                        💡 Bills
                    </option>

                    <option
                        value="Entertainment"
                        {% if form_category == "Entertainment" %}selected{% endif %}
                    >
                        🎬 Entertainment
                    </option>

                    <option
                        value="Health"
                        {% if form_category == "Health" %}selected{% endif %}
                    >
                        🏥 Health
                    </option>

                    <option
                        value="Other"
                        {% if form_category == "Other" %}selected{% endif %}
                    >
                        📦 Other
                    </option>

                </select>

            </div>



            <!-- Add button -->

            <button
                class="add-button"
                type="submit"
            >
                Add Expense
            </button>


        </form>

    </div>



    <!-- -------------------------------------------------
         Expense list
    -------------------------------------------------- -->

    <div class="card">

        <h2>📋 Recent Expenses</h2>


        {% if expenses %}


        <table>

            <thead>

                <tr>

                    <th>Description</th>

                    <th>Category</th>

                    <th>Amount</th>

                    <th>Action</th>

                </tr>

            </thead>


            <tbody>


                {% for expense in expenses %}


                <tr>


                    <td>
                        {{ expense.description }}
                    </td>


                    <td>

                        <span class="category">

                            {{ category_icons.get(
                                expense.category,
                                "📦"
                            ) }}

                            {{ expense.category }}

                        </span>

                    </td>


                    <td class="amount">

                        RM {{ "%.2f"|format(expense.amount) }}

                    </td>


                    <td>


                        <form
                            method="POST"
                            action="/delete/{{ expense.id }}"
                            onsubmit="return confirmDelete(
                                '{{ expense.description }}'
                            )"
                        >

                            <button
                                class="delete-button"
                                type="submit"
                            >
                                🗑️ Delete
                            </button>

                        </form>


                    </td>


                </tr>


                {% endfor %}


            </tbody>

        </table>


        {% else %}


        <div class="empty-state">

            <div class="emoji">🧾</div>

            <h3>No expenses yet</h3>

            <p>
                Add your first expense using the form above.
            </p>

        </div>


        {% endif %}



        <div class="docker-status">

            🐳 Docker Web Application Running

        </div>


    </div>



    <!-- -------------------------------------------------
         Footer
    -------------------------------------------------- -->

    <footer>

        Developed by Thivyasree A/P Sunder |
        Student ID: 105685114

        <br>

        Python Flask + Docker

    </footer>


</div>



<script>


    /* -------------------------------------------------
       Delete confirmation
    -------------------------------------------------- */

    function confirmDelete(description) {

        return confirm(
            'Are you sure you want to delete "' +
            description +
            '"?'
        );

    }



    /* -------------------------------------------------
       Hide success/delete notifications after 2 seconds
    -------------------------------------------------- */

    setTimeout(function () {

        const notifications =
            document.querySelectorAll('.auto-hide');


        notifications.forEach(function (notification) {

            notification.style.opacity = '0';


            setTimeout(function () {

                notification.remove();

            }, 400);

        });


    }, 2000);


</script>


</body>

</html>
"""


# ---------------------------------------------------------
# Helper function to render page
# ---------------------------------------------------------
def render_page(
    description_error="",
    amount_error="",
    form_description="",
    form_amount="",
    form_category="Food"
):

    total = sum(
        expense["amount"]
        for expense in expenses
    )


    return render_template_string(
        HTML,
        expenses=expenses,
        total=total,
        category_icons=category_icons,
        description_error=description_error,
        amount_error=amount_error,
        form_description=form_description,
        form_amount=form_amount,
        form_category=form_category
    )



# ---------------------------------------------------------
# Home page
# ---------------------------------------------------------
@app.route("/")
def home():

    return render_page()



# ---------------------------------------------------------
# Add expense
# ---------------------------------------------------------
@app.route("/add", methods=["POST"])
def add_expense():


    description = request.form.get(
        "description",
        ""
    ).strip()


    amount_text = request.form.get(
        "amount",
        ""
    ).strip()


    category = request.form.get(
        "category",
        "Other"
    )



    # -----------------------------------------------------
    # Description validation
    # -----------------------------------------------------

    if not description:

        return render_page(
            description_error="Please enter an expense description.",
            form_description=description,
            form_amount=amount_text,
            form_category=category
        )



    # -----------------------------------------------------
    # Amount validation
    # -----------------------------------------------------

    if not amount_text:

        return render_page(
            amount_error="Please enter an amount.",
            form_description=description,
            form_amount=amount_text,
            form_category=category
        )



    try:

        amount = float(amount_text)


    except ValueError:

        return render_page(
            amount_error="Please enter a valid numerical amount.",
            form_description=description,
            form_amount=amount_text,
            form_category=category
        )



    if amount <= 0:

        return render_page(
            amount_error="Amount must be greater than RM 0.",
            form_description=description,
            form_amount=amount_text,
            form_category=category
        )



    # -----------------------------------------------------
    # Generate new expense ID
    # -----------------------------------------------------

    new_id = max(
        [expense["id"] for expense in expenses],
        default=0
    ) + 1



    # -----------------------------------------------------
    # Add expense
    # -----------------------------------------------------

    expenses.append({

        "id": new_id,

        "description": description,

        "amount": amount,

        "category": category

    })



    # Green success notification

    flash(
        f'Expense "{description}" was added successfully!',
        "success"
    )


    # Redirect clears form after successful addition

    return redirect("/")



# ---------------------------------------------------------
# Delete expense
# ---------------------------------------------------------
@app.route(
    "/delete/<int:expense_id>",
    methods=["POST"]
)
def delete_expense(expense_id):


    expense = next(

        (
            item
            for item in expenses
            if item["id"] == expense_id
        ),

        None

    )



    if expense is None:

        return redirect("/")



    expenses.remove(expense)



    # RED notification for deletion

    flash(
        f'Expense "{expense["description"]}" was deleted successfully!',
        "deleted"
    )


    return redirect("/")



# ---------------------------------------------------------
# Start Flask application
# ---------------------------------------------------------
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8080,
        debug=False
    )