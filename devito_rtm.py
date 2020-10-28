import numpy as np
import pytest

from devito.logger import info
from devito import Constant, Function, smooth, norm
from examples.seismic.acoustic import AcousticWaveSolver
from examples.seismic import demo_model, setup_geometry, seismic_args


def acoustic_setup(shape=(50, 50, 50), spacing=(15.0, 15.0, 15.0),
                   tn=500., kernel='OT2', space_order=4, nbl=10,
                   preset='layers-isotropic', fs=False, **kwargs):
    model = demo_model(preset, space_order=space_order, shape=shape, nbl=nbl,
                       dtype=kwargs.pop('dtype', np.float32), spacing=spacing,
                       fs=fs, **kwargs)

    # Source and receiver geometries
    geometry = setup_geometry(model, tn)

    # Create solver object to provide relevant operators
    solver = AcousticWaveSolver(model, geometry, kernel=kernel,
                                space_order=space_order, **kwargs)
    return solver


def run(shape=(50, 50, 50), spacing=(20.0, 20.0, 20.0), tn=1000.0,
        space_order=4, kernel='OT2', nbl=40, full_run=False, fs=False,
        autotune=False, preset='layers-isotropic', checkpointing=False, **kwargs):

    solver = acoustic_setup(shape=shape, spacing=spacing, nbl=nbl, tn=tn,
                            space_order=space_order, kernel=kernel, fs=fs,
                            preset=preset, **kwargs)

    info("Applying Forward")
    rec, u, summary = solver.forward(save=True, autotune=autotune)

    info("Applying Gradient")
    solver.jacobian_adjoint(rec, u, autotune=autotune, checkpointing=checkpointing)
    return summary.gflopss, summary.oi, summary.timings, [rec, u.data]


if __name__ == "__main__":
    description = ("Example script for a set of acoustic operators.")
    parser = seismic_args(description)
    parser.add_argument('--fs', dest='fs', default=False, action='store_true',
                        help="Whether or not to use a freesurface")
    parser.add_argument("-k", dest="kernel", default='OT2',
                        choices=['OT2', 'OT4'],
                        help="Choice of finite-difference kernel")
    args = parser.parse_args()

    # 3D preset parameters
    ndim = 2
    shape = args.shape[:ndim]
    spacing = tuple(ndim * [15.0])
    tn = args.tn if args.tn > 0 else (750. if ndim < 3 else 1250.)

    preset = 'constant-isotropic' if args.constant else 'layers-isotropic'
    run(shape=shape, spacing=spacing, nbl=args.nbl, tn=tn, fs=args.fs,
        space_order=args.space_order, preset=preset, kernel=args.kernel,
        autotune=args.autotune, opt=args.opt, full_run=args.full,
        checkpointing=args.checkpointing, dtype=args.dtype)
