from controller import loginAPI


def routes(api):
    api.add_resource(loginAPI, '/login',endpoint= 'login')