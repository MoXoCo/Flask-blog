from app import app

if __name__ == '__main__':
    '''
    args = {
        'port': 11000,
        'debug': True,
        'host': '0.0.0.0',
    }
    app.run(**args)
'''
    app.run(debug=True)