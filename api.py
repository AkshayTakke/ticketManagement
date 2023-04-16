from controller import loginAPI, logout, homePage, tickets, createTicket, dashboard


def routes(api):
    api.add_resource(loginAPI, '/login', endpoint='login')
    api.add_resource(logout, '/logout')
    api.add_resource(homePage, '/')
    api.add_resource(tickets, '/tickets', methods=['GET', 'POST', 'DELETE'])
    api.add_resource(createTicket, '/create_ticket', endpoint='create_ticket')
    api.add_resource(dashboard, '/dashboard', endpoint='dashboard')
