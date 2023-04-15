from controller import loginAPI,logoutx 


def routes(api):
    api.add_resource(loginAPI, '/login',endpoint= 'login')
    api.add_resource(logout, '/logout')
