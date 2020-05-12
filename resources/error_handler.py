from flask import render_template


def page_not_found(e):
    """Функция для открытия страницы с показом ошибки 404"""
    return render_template('404.html')
