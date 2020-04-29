from plugins import Plugin
import wtferrors
import subprocess

class Service(Plugin):

    @classmethod
    def get_aliases(cls):
        return ["service"]

    def any(self, params):
        self._validate_params(params, ['state', 'name'], 'service')
        if params.get('state') not in ['running', 'stopped']:
            raise wtferrors.UnrecognizedParamValue('state', params.get('state'), 'service', 'running, stopped')

        status_code= subprocess.call(['systemctl', 'status', params.get('name')])

        if params.get('state') == 'running':
            if status_code == 3:
                start_status_code = subprocess.call(['systemctl', 'start', params.get('name')])
                if start_status_code != 0:
                    raise wtferrors.CriticalFunctionFailure('service', 'Starting the service returned status code {}'.format(start_status_code))
                return True, None
            elif status_code == 0:
                return False, "The service '{}' appears to already be running.".format(params.get('name'))
            else:
                raise wtferrors.CriticalFunctionFailure('service', "The status of service '{}' returned unexpected status code: {}".format(params.get('name'), status_code))
        elif params.get('state') == 'stopped':
            if status_code == 0:
                stop_status_code = subprocess.call(['systemctl', 'stop', params.get('name')])
                if stop_status_code != 0:
                    raise wtferrors.CriticalFunctionFailure('service', 'Stopping the service returned status code {}'.format(stop_status_code))
                return True, None
            elif status_code == 3:
                return False, "The service '{}' appears to already be stopped.".format(params.get('name'))
            else:
                raise wtferrors.CriticalFunctionFailure('service',
                                                        "The status of service '{}' returned unexpected status code: {}".format(
                                                            params.get('name'), status_code))
        else:
            raise wtferrors.UnrecognizedParamValue('state', params.get('state'), 'service', 'running, stopped')



