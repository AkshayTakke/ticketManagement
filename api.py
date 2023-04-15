from controller import loginAPI,logout,homePage


def routes(api):
    api.add_resource(loginAPI, '/login',endpoint= 'login')
    api.add_resource(logout, '/logout')
    api.add_resource(homePage, '/')
