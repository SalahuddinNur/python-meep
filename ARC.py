# ARC Simulation

from __future__ import division

import argparse
import meep as mp
import script
import time

def main(args):
    sx=10
    sy=10
    eps_Si=12
    eps=4
    T_Si=1
    T_Arc=float(args.v)
    cell = mp.Vector3(sx, sy, 0)
    pml_layers = [mp.PML(1.0)]
    resolution = 10
    nfreq = 100
        fcen = 0.15  # pulse center frequency
        df = 0.1  # pulse width (in frequency)

    print(T_Arc)

    if args.no_ARC:
        geometry = [mp.Block(mp.Vector3(sx, sy, mp.inf), center=mp.Vector3(0, 0),
            material=mp.Medium(epsilon=1))]
    else:
        geometry = [mp.Block(mp.Vector3(T_Si, sy, mp.inf), center=mp.Vector3(0, 0),
            material=mp.Medium(epsilon=eps_Si)),
                mp.Block(mp.Vector3(T_Arc, sy, mp.inf), center=mp.Vector3(-0.5 * (T_Si + T_Arc), 0),
                    material=mp.Medium(epsilon=eps))]

    sources = [mp.Source(mp.GaussianSource(fcen, fwidth=df), component=mp.Ez,
                center=mp.Vector3(2 + (-0.5 * sx), 0), size=mp.Vector3(0, 1))]
    sim = mp.Simulation(cell_size=cell,
            boundary_layers=pml_layers,
            geometry=geometry,
            sources=sources,
            resolution=resolution)

    if args.no_ARC:
        fr = mp.FluxRegion(center=mp.Vector3((T_Si / 2) - (T_Si / 100), 0), size=mp.Vector3(0, sy))
    else:
        fr = mp.FluxRegion(center=mp.Vector3((T_Si / 2) - (T_Si / 100), 0), size=mp.Vector3(0, sy))

    trans = sim.add_flux(fcen, df, nfreq, fr)

    refl_fr = mp.FluxRegion(center=mp.Vector3((-0.5 * sx) + 1, 0),size=mp.Vector3(0, sy))

    # reflected flux
    refl = sim.add_flux(fcen, df, nfreq, refl_fr)

    # for normal run, load negated fields to subtract incident from refl. fields
    if not args.no_ARC:
        sim.load_minus_flux('refl-flux', refl)

    if args.no_ARC:
        pt = mp.Vector3((T_Si / 2) - (T_Si / 100), 0)
    else:
        pt = mp.Vector3((T_Si / 2) - (T_Si / 100), 0)

    sim.run(mp.at_beginning(mp.output_epsilon),until_after_sources=mp.stop_when_fields_decayed(50, mp.Ez, pt, 1e-3))

    	# for normalization run, save flux fields for refl. plane
    if args.no_ARC:
        sim.save_flux('refl-flux', refl)

    sim.display_fluxes(trans, refl)

def test(inputv):
    print(inputv)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--no_ARC', action='store_true', default=False,
					help="Straight waveguide without bend.")
    parser.add_argument('-v')
    args = parser.parse_args()
    #print(script.readArg())
    start_time = time.time()
    main(args)
    print("eclipsed time : %d"  %(time.time() - start_time))
