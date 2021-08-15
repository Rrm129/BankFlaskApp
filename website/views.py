from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Transaction
from . import db
import json
import time

views = Blueprint('views', __name__)


@views.route('/')
def start_app():
    return redirect(url_for('auth.login'))


@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    transaction_list= []

    for transaction in current_user.transactions:
        transaction_list.append(transaction)
    # current_user.transactions.reverse()
    # print(current_user.transactions)
    transaction_list.reverse()
    # if request.method == 'POST':
    #     note = request.form.get('note')

    #     if len(note) < 2:
    #         flash('Note is too short!', category='error')
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash('Note added', category='success')

    return render_template("home.html", user=current_user, transaction_list=transaction_list)


@views.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    if request.method == 'POST':
        amount = request.form.get('amount')      
        try:   
            amount = int(amount)
            new_transaction = Transaction(transaction_type='D',\
                amount=amount, user_id=current_user.id)
            current_user.balance = current_user.balance + amount
            db.session.add(new_transaction)
            db.session.commit()
            flash('Transaction Completed!', category='success')
        except:
            
            flash('Invalid', category='error')

    return render_template("deposit.html", user=current_user)

@views.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    if request.method == 'POST':
        amount = request.form.get('amount')
        try:
            amount = int(amount)
            new_transaction = Transaction(transaction_type='T',
                                          amount=amount, user_id=current_user.id)
            current_user.balance = current_user.balance - amount
            db.session.add(new_transaction)
            db.session.commit()
            flash('Transaction Completed!', category='success')
        except:
            flash('Invalid', category='error')

    return render_template("transfer.html", user=current_user)

# @views.route('/delete-note', methods=['POST'])
# @login_required
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()
#             return jsonify({})
