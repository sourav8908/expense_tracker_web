from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from wtforms import Form, DecimalField, StringField, DateField, SelectField, validators
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production!

# MySQL connection info
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'expense_user'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'expense_tracker_db'

mysql = MySQL(app)

# Expense Form with validation
class ExpenseForm(Form):
    amount = DecimalField('Amount', [validators.InputRequired(), validators.NumberRange(min=0.01)])
    expense_date = DateField('Date', [validators.InputRequired()], format='%Y-%m-%d', default=datetime.today)
    note = StringField('Note', [validators.Length(max=255)])
    category = SelectField('Category', choices=[('Food', 'Food'), ('Travel', 'Travel'), ('Bills', 'Bills'), ('Other', 'Other')])

# Home page with filtering
@app.route('/')
def index():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category = request.args.get('category')

    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT category FROM expenses")
    categories = [row[0] for row in cur.fetchall() if row[0]]

    query = "SELECT id, amount, expense_date, note, category FROM expenses WHERE 1=1"
    params = []

    if start_date:
        query += " AND expense_date >= %s"
        params.append(start_date)
    if end_date:
        query += " AND expense_date <= %s"
        params.append(end_date)
    if category and category != "":
        query += " AND category = %s"
        params.append(category)

    query += " ORDER BY expense_date DESC"

    cur.execute(query, tuple(params))
    expenses = cur.fetchall()
    cur.close()

    return render_template('index.html', expenses=expenses, categories=categories)

# Add new expense
@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    form = ExpenseForm(request.form)
    if request.method == 'POST' and form.validate():
        amount = form.amount.data
        expense_date = form.expense_date.data.strftime('%Y-%m-%d')
        note = form.note.data
        category = form.category.data
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO expenses(amount, expense_date, note, category) VALUES(%s, %s, %s, %s)",
                    (amount, expense_date, note, category))
        mysql.connection.commit()
        cur.close()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_expense.html', form=form)

# Edit expense
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT amount, expense_date, note, category FROM expenses WHERE id = %s", (id,))
    expense = cur.fetchone()
    cur.close()
    if not expense:
        flash('Expense not found.', 'danger')
        return redirect(url_for('index'))

    form = ExpenseForm(request.form, data={
        'amount': expense[0],
        'expense_date': expense[1],
        'note': expense[2],
        'category': expense[3]
    })

    if request.method == 'POST' and form.validate():
        amount = form.amount.data
        expense_date = form.expense_date.data.strftime('%Y-%m-%d')
        note = form.note.data
        category = form.category.data
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE expenses SET amount=%s, expense_date=%s, note=%s, category=%s WHERE id=%s",
                    (amount, expense_date, note, category, id))
        mysql.connection.commit()
        cur.close()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit_expense.html', form=form, id=id)

# Delete expense
@app.route('/delete/<int:id>', methods=['POST'])
def delete_expense(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM expenses WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('index'))

# Summary Report Page
@app.route('/summary')
def summary():
    cur = mysql.connection.cursor()

    # Total spending
    cur.execute("SELECT SUM(amount) FROM expenses")
    total_spent = cur.fetchone()[0] or 0

    # Spending by category
    cur.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    category_summary = cur.fetchall()

    # Spending by month
    cur.execute("""
        SELECT DATE_FORMAT(expense_date, '%Y-%m') AS month, SUM(amount)
        FROM expenses
        GROUP BY month
        ORDER BY month DESC
    """)
    monthly_summary = cur.fetchall()

    cur.close()

    return render_template('summary.html',
                           total_spent=total_spent,
                           category_summary=category_summary,
                           monthly_summary=monthly_summary)

if __name__ == '__main__':
    app.run(debug=True)
