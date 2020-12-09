from pyhunter import PyHunter
import clearbit

from config import Api_conf


def hunter_email_verifier(email):
    print(Api_conf.hunter_key)
    hunter_data = PyHunter(Api_conf.hunter_key)
    try:
        email_status = hunter_data.email_verifier(email)
        if email_status['score'] >= 50:
            return True
    except Exception as e:
        print(e)
    return False


def clearbit_email_data(email):
    print(Api_conf.clearbit_key)
    clearbit.key = Api_conf.clearbit_key
    clearbit_data = clearbit.Enrichment.find(email=email, stream=True)
    try:
        return {
                'first_name': clearbit_data['person']['name']['givenName'],
                'last_name': clearbit_data['person']['name']['familyName']
                }
    except:
        return False
