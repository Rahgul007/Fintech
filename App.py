from Settings import *

from Api.Teams_Details.Models import *
from Api.Funds_Details.Models import *
from Api.Service_Details.Models import *
from Api.Service_Details.Payment.Models import *
from Api.Account_Details.Models import *
from Api.Settings_Details.Models import *
from Api.Auth.Models import *
from Api.Jobs.Models import *
from Api.Settings_Details.Models import *




from Api.Auth.Views.App_user import *
from Api.Teams_Details.Views.Employee import *
from Api.Teams_Details.Views.Member_profile import *
from Api.Teams_Details.Views.Leader_profile import *
from Api.Funds_Details.Views.Santha_payment import *
from Api.Funds_Details.Views.Member_savings import *
from Api.Service_Details.Views.Request_details import *
# from Api.Services_Details.Views.Savings_loan import *
# from Api.Services_Details.Views.Business_loan import *
# from Api.Services_Details.Views.Education_loan import *
# from Api.Services_Details.Views.Pension_details import *
# from Api.Services_Details.Views.Benefits_details import *
# from Api.Auth.Views.Login import *
# from Api.Services_Details.Payment.Views.Business_loan_payment import *
# from Api.Services_Details.Payment.Views.Distributed_benefit import *
# from Api.Services_Details.Payment.Views.Education_loan_payment import *
# from Api.Services_Details.Payment.Views.Pension_payment import *
# from Api.Services_Details.Payment.Views.Savings_loan_payment import *
# from Api.Jobs.Views import *
# from Api.Search_bar.Search import *
# from Api.Settings_Details.Views.Meta_details import *


if '__main__' == __name__:  
    # scheduler.add_job(id="first-run",func=Savings_job,trigger='interval',seconds=5)
    # # scheduler.add_job(id="second-run",func=call, trigger='cron', hour='22', minute='30')
    # scheduler.start()
    app.run(debug=True)