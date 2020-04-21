from .add_adduct import add_adduct
from .correct_charge import correct_charge
from .derive_ionmode import derive_ionmode
from .make_charge_scalar import make_charge_scalar
from .make_ionmode_lowercase import make_ionmode_lowercase
from .set_ionmode_na_when_missing import set_ionmode_na_when_missing


def default_filters(spectrum):
    spectrum = make_charge_scalar(spectrum)
    spectrum = make_ionmode_lowercase(spectrum)
    spectrum = set_ionmode_na_when_missing(spectrum)
    spectrum = add_adduct(spectrum)
    spectrum = derive_ionmode(spectrum)
    spectrum = correct_charge(spectrum)
    return spectrum