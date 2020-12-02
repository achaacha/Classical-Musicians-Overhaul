from injector import inject_to
from index import iover
from sims4.tuning.instance_manager import InstanceManager
from sims4.resources import Types
import services

@inject_to(InstanceManager, 'load_data_into_class_instances')
def Acha_InstrumentOverhaul_on_instance_manager_loaded(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        if self.TYPE == Types.OBJECT:
            injections_by_sa = [
                {
                    "interactions": (iover.piano.LIVE,),
                    "sas": (iover.piano.PRAC,)
                },
            ]
            for injection in injections_by_sa:
                Acha_InstrumentOverhaul_inject_interactions_by_sas(self, interactions=injection['interactions'], sas=['sas'])
    except Exception as e:
        raise Exception(f'Error IO: {str(e)}')
    return result

def Acha_InstrumentOverhaul_inject_interactions_by_sas(self, interactions=None, sas=None):
    affordance_manager = services.get_instance_manager(Types.INTERACTION)
    interactions_tuning = tuple(filter(lambda a: a, [affordance_manager.get(a) for a in interactions]))
    sas_tuning = tuple(filter(lambda sa: sa, [affordance_manager.get(sa) for sa in sas]))

    if not interactions_tuning or not sas_tuning:
        return

    def has_some_sa(sa_list):
        for sa in sas_tuning:
            if sa in sa_list:
                return True
        return False

    for _, obj_tuning in self._tuned_classes.items():
        if hasattr(obj_tuning, '_super_affordances') and has_some_sa(obj_tuning._super_affordances):
            obj_tuning._super_affordances = obj_tuning._super_affordances + interactions_tuning