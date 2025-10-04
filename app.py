from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from wtforms import Form, DecimalField, StringField, DateField, SelectField, validators
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # You can change this

# MySQL connection info
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'expense_user'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'expense_tracker_db'

mysql = MySQL(app)

# Define the form used for input validation
class ExpenseForm(Form):
    amount = DecimalField('Amount', [validators.InputRequired(), validators.NumberRange(min=0.01)])
    expense_date = DateField('Date', [validators.InputRequired()], format='%Y-%m-%d', default=datetime.today)
    note = StringField('Note', [validators.Length(max=255)])
    category = SelectField('Category', choices=[('Food', 'Food'), ('Travel', 'Travel'), ('Bills', 'Bills'), ('Other', 'Other')])

# Home page - list all expenses
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, amount, expense_date, note, category FROM expenses ORDER BY expense_date DESC")
    expenses = cur.fetchall()
    cur.close()
    return render_template('index.html', expenses=expenses)

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

if __name__ == '__main__':
    app.run(debug=True)
