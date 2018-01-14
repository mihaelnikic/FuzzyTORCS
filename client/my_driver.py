from client.pytocl.driver import Driver

from client.pytocl.car import State, Command
from defuzzy.coa_def import COADefuzzifier
from defuzzy.cog_def import COGDefuzzifier
from engine.inf_eng import InferenceEngine
from fuzzy.zadeh.binary_zadeh_or import ZadehOr
from fuzzy.zadeh.zadeh_and import ZadehAnd
from fuzzy.zadeh.zadeh_not import ZadehNot

from parser.rule_loader import load_rules_from_files
from property.properties_loader import load_properties_two_files

MODIFIERS_FILE = '../property/modifiers'
PARAMS_FILE = '../property/params'
COG = COGDefuzzifier()
COA = COADefuzzifier()
AND = ZadehAnd()
OR = ZadehOr()
NOT = ZadehNot()
CONTROL_PARAMS = {'AKCELERACIJA': COG, 'KOČNICA': COG,
                  'MJENJAČ': COA, 'VOLAN': COG,
                  'FOKUS_SMJER': COG}


class MyDriver(Driver):
    def __init__(self, rule_base_path, args, logdata=True):
        super().__init__(logdata=logdata)
        self.rules_dict = load_rules_from_files(rule_base_path)
        self.properties = load_properties_two_files(MODIFIERS_FILE, PARAMS_FILE)
        self.engines = {}
        for control_p in CONTROL_PARAMS:
            if control_p in self.rules_dict:
                self.engines[control_p] = InferenceEngine(self.rules_dict, self.properties,
                                                          control_p, AND, OR,
                                                          AND, NOT, CONTROL_PARAMS[control_p])
        self.default_args = {'AKCELERACIJA': args.AKCELERACIJA, 'KOČNICA': args.KOCNICA,
                             'MJENJAČ': args.MJENJAC, 'VOLAN': args.VOLAN, 'FOKUS_SMJER': args.FOKUS}

    # Override the `drive` method to create your own driver
    def drive(self, carstate: State) -> Command:
        # Interesting stuff
        command = Command()
        command.accelerator = self.fire('AKCELERACIJA', carstate)
        command.brake = self.fire('KOČNICA', carstate)
        command.gear = self.fire('MJENJAČ', carstate)
        command.steering = self.fire('VOLAN', carstate)
        command.focus = self.fire('FOKUS_SMJER', carstate)
        return command

    def fire(self, param_name, state):
        if param_name in self.engines:
            state_values = dict(
                KUT=state.angle,
                TRENUTNO_VRIJEME_KRUGA=state.current_lap_time,
                OŠTEĆENJE=state.damage,
                UDALJENOST_OD_STARTA=state.distance_from_start,
                PRIJEĐENI_PUT=state.distance_raced,
                PREOSTALO_BENZINA=state.fuel,
                MJENAČ=state.fuel,
                VRIJEME_PROŠLOG_KRUGA=state.last_lap_time,
                POZICIJA=state.race_position,
                RPM=state.rpm,
                BRZINA_X=state.speed_x,
                BRZINA_Y=state.speed_y,
                BRZINA_Z=state.speed_z,
                UNUTAR_TRAKE=state.distance_from_center,
                UDALJENOST_OD_TLA=state.z
            )
            self.add_vector_values(state_values, "FOKUSIRANA_UDALJENOST_SENZOR", state.focused_distances_from_edge)
            self.add_vector_values(state_values, "UDALJENOST_PROTIVNIKA_SENZOR", state.opponents)
            self.add_vector_values(state_values, "UDALJENOST_STAZE_SENZOR", state.distances_from_edge)
            self.add_vector_values(state_values, "ROTACIJSKA_BRZINA_SENZOR", state.wheel_velocities)
            return self.engines[param_name].infer(state_values)
        return self.default_args[param_name]

    def add_vector_values(self, state_values, name, vector):
        for i, value in enumerate(vector):
            state_values[name + str(i)] = value
