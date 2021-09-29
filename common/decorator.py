import logging

from django.http import HttpResponseRedirect

logger = logging.getLogger('dev')

admin_login = '/admin/login'


def admin_login_required(function):
    def wrapper(request, *args, **kwargs):
        logger.info("admin_login_required wrapper")
        if request.user.is_authenticated:
            logger.info(request.user.id)
            if request.user.is_admin or request.user.is_superuser:
                return function(request, *args, **kwargs)
            logger.info('{0} is not admin'.format(request.user.id))
            return HttpResponseRedirect(admin_login)
        else:
            logger.info("authenticate failed")
            return HttpResponseRedirect(admin_login)

    return wrapper
