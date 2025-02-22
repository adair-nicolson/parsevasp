"""Test xml parsee, the event based extraction.

 This mode only supports properly terminated XML files.

"""
import os

import numpy as np
import pytest

from parsevasp.vasprun import Xml


@pytest.fixture
def xml_parser(request):
    """Load XML file. Test only terminated XML.

    """
    filename = request.param
    testdir = os.path.dirname(__file__)
    xmlfile = os.path.join(testdir, filename)
    xml = Xml(xmlfile, event=True)

    return xml


@pytest.mark.parametrize('xml_parser', ['basic.xml'], indirect=True)
def test_xml_exist(xml_parser):
    """Check if xml_parser exists.

    """
    assert xml_parser.get_dict()


@pytest.mark.parametrize('xml_parser', ['gw.xml'], indirect=True)
def test_xml_energies_gw(xml_parser):
    """Check total energies not present for GW runs.

    """
    import numpy as np

    energies_data = xml_parser.get_energies('initial')
    assert energies_data is None


@pytest.mark.parametrize('xml_parser', ['basic.xml'], indirect=True)
def test_xml_energies(xml_parser):
    """Check total energies for runs with no ionic steps.

    """
    import numpy as np

    energies_data = xml_parser.get_energies('initial')
    test_array_energies = np.array([-43.312106219999997])
    test_array_steps = np.array([1], dtype=int)
    assert np.allclose(test_array_energies, energies_data['energy_extrapolated'])
    assert np.allclose(test_array_steps, energies_data['electronic_steps'])
    energy_data = xml_parser.get_energies('last')
    assert np.allclose(test_array_energies, energies_data['energy_extrapolated'])
    assert np.allclose(test_array_steps, energies_data['electronic_steps'])
    energies_data = xml_parser.get_energies('all')
    assert np.allclose(test_array_energies, energies_data['energy_extrapolated'])
    assert np.allclose(test_array_steps, energies_data['electronic_steps'])
    test_array_energies = np.array([-0.00053151])
    # Notice that the test have here used results from VASP 5, which has a bug in the xml
    # prints for the final energies. In VASP 6 this bug is fixed.
    assert np.allclose(test_array_energies, energies_data['energy_extrapolated_final'])


@pytest.mark.parametrize('xml_parser', ['basicrelax.xml'], indirect=True)
def test_xml_energies_ionic(xml_parser):
    """Check total energies for runs with ionic steps.

    """
    import numpy as np

    energies_data = xml_parser.get_energies('initial')
    test_array_steps = np.array([1], dtype=int)
    test_array_energies = np.array([-42.91113348])
    assert np.allclose(test_array_energies, energies_data['energy_extrapolated'])
    assert np.allclose(test_array_steps, energies_data['electronic_steps'])
    energies_data = xml_parser.get_energies('last')
    test_array_energies = np.array([-43.39087657])
    assert np.allclose(test_array_energies, energies_data['energy_extrapolated'])
    assert np.allclose(test_array_steps, energies_data['electronic_steps'])
    energies_data = xml_parser.get_energies('all')
    test_array_energies = np.array([
        -42.91113348, -43.27757545, -43.36648855, -43.37734069, -43.38062479, -43.38334165, -43.38753003, -43.38708193,
        -43.38641449, -43.38701639, -43.38699488, -43.38773717, -43.38988315, -43.3898822, -43.39011239, -43.39020751,
        -43.39034244, -43.39044584, -43.39087657
    ])
    test_array_steps = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=int)
    assert np.allclose(test_array_energies, energies_data['energy_extrapolated'])
    assert len(energies_data['electronic_steps']) == len(energies_data['energy_extrapolated'])
    assert np.allclose(test_array_steps, energies_data['electronic_steps'])
    test_array_energies = np.array([
        -0.00236637, -0.00048614, -0.00047201, -0.00043261, -0.00041668, -0.00042584, -0.00043637, -0.00042806,
        -0.00042762, -0.00043875, -0.00042731, -0.00042705, -0.00043064, -0.00043051, -0.00043161, -0.00043078,
        -0.00043053, -0.00043149, -0.00043417
    ])
    # Notice that the test have here used results from VASP 5, which has a bug in the xml
    # prints for the final energies. In VASP 6 this bug is fixed.
    assert np.allclose(test_array_energies, energies_data['energy_extrapolated_final'])


@pytest.mark.parametrize('xml_parser', ['basic.xml'], indirect=True)
def test_xml_energies_electronic(xml_parser):
    """Check total energies for runs without ionic steps, for each electronic step.

    """
    import numpy as np

    energies_data = xml_parser.get_energies('all', nosc=False)
    test_array_energies = np.array([
        34.33397233, -40.91109366, -43.93640589, -43.97897688, -43.98005344, -43.52006123, -43.30797519, -43.31109453,
        -43.31199447, -43.31209931, -43.31210726, -43.31210622
    ])
    test_array_steps = np.array([12], dtype=int)
    assert np.allclose(test_array_energies, energies_data['energy_extrapolated'])
    assert np.allclose(test_array_steps, energies_data['electronic_steps'])
    energies_data = xml_parser.get_energies('last', nosc=False)
    assert np.allclose(test_array_energies, energies_data['energy_extrapolated'])
    assert np.allclose(test_array_steps, energies_data['electronic_steps'])
    energies_data = xml_parser.get_energies('all', nosc=False)
    assert np.allclose(test_array_energies, energies_data['energy_extrapolated'])
    assert np.allclose(test_array_steps, energies_data['electronic_steps'])
    test_array_energies = np.array([-0.00053151])
    assert np.allclose(test_array_energies, energies_data['energy_extrapolated_final'])


@pytest.mark.parametrize('xml_parser', ['basicrelax.xml'], indirect=True)
def test_xml_energies_ionic_sc(xml_parser):
    """Check total energies for runs with ionic steps, for each electronic step.

    """
    import numpy as np

    energies_data = xml_parser.get_energies('initial', nosc=False)
    test_array_energies = np.array([
        163.37398579, 14.26925896, -23.05190509, -34.91615104, -40.20080347, -42.18390876, -42.97469852, -43.31556073,
        -43.60169068, -43.61723125, -43.61871511, -43.61879751, -43.12548175, -42.90647187, -42.91031846, -42.91099027,
        -42.91111107, -42.91113348
    ])
    test_array_steps = np.array([18], dtype=int)
    assert np.allclose(test_array_energies, energies_data['energy_extrapolated'])
    assert np.allclose(test_array_steps, energies_data['electronic_steps'])
    energies_data = xml_parser.get_energies('last', nosc=False)
    test_array_energies = np.array([-43.39084354, -43.39088709, -43.39087657])
    test_array_steps = np.array([3], dtype=int)
    assert np.allclose(test_array_energies, energies_data['energy_extrapolated'])
    assert np.allclose(test_array_steps, energies_data['electronic_steps'])
    energies_data = xml_parser.get_energies('all', nosc=False)
    test_array_energies = [
        np.array([
            163.37398579, 14.26925896, -23.05190509, -34.91615104, -40.20080347, -42.18390876, -42.97469852,
            -43.31556073, -43.60169068, -43.61723125, -43.61871511, -43.61879751, -43.12548175, -42.90647187,
            -42.91031846, -42.91099027, -42.91111107, -42.91113348
        ]),
        np.array([-43.34236449, -43.31102002, -43.27768275, -43.27791002, -43.27761357, -43.27757545]),
        np.array([-43.40320524, -43.38084022, -43.36835045, -43.36666248, -43.36666583, -43.36649036, -43.36648855]),
        np.array([-43.37749056, -43.37749102, -43.37734414, -43.37734069]),
        np.array([-43.38117265, -43.38082881, -43.38063293, -43.38062479]),
        np.array([-43.38337336, -43.38334165]),
        np.array([-43.38778922, -43.38766017, -43.38752953, -43.38753003]),
        np.array([-43.38714489, -43.38708193]),
        np.array([-43.38640951, -43.38641449]),
        np.array([-43.3874799, -43.3871553, -43.38701949, -43.38701639]),
        np.array([-43.38790942, -43.38727062, -43.38700335, -43.38699488]),
        np.array([-43.38774394, -43.38773717]),
        np.array([-43.38984942, -43.3899134, -43.38988315]),
        np.array([-43.38988117, -43.3898822]),
        np.array([-43.39032165, -43.39017866, -43.39011239]),
        np.array([-43.39021044, -43.39020751]),
        np.array([-43.39034135, -43.39034244]),
        np.array([-43.39044466, -43.39044584]),
        np.array([-43.39084354, -43.39088709, -43.39087657])
    ]
    test_array_steps = np.array([18, 6, 7, 4, 4, 2, 4, 2, 2, 4, 4, 2, 3, 2, 3, 2, 2, 2, 3])
    # Build a flattened array (not using flatten from NumPy as the content is staggered) and
    # test number of electronic steps per ionic step
    test_array_energies_flattened = np.array([])
    for index, ionic_step in enumerate(test_array_energies):
        test_array_energies_flattened = np.append(test_array_energies_flattened, ionic_step)
    assert np.allclose(test_array_energies_flattened, energies_data['energy_extrapolated'])
    assert np.allclose(test_array_steps, energies_data['electronic_steps'])
    test_array_energies = np.array([
        -0.00236637, -0.00048614, -0.00047201, -0.00043261, -0.00041668, -0.00042584, -0.00043637, -0.00042806,
        -0.00042762, -0.00043875, -0.00042731, -0.00042705, -0.00043064, -0.00043051, -0.00043161, -0.00043078,
        -0.00043053, -0.00043149, -0.00043417
    ])
    assert np.allclose(test_array_energies, energies_data['energy_extrapolated_final'])


@pytest.mark.parametrize('xml_parser', ['basic.xml'], indirect=True)
def test_xml_forces(xml_parser):
    """Check forces.

    """

    forces = xml_parser.get_forces('initial')
    test = np.array([[0., -0., 0.], [0., 0., -0.], [-0., 0., -0.], [-0., 0., 0.], [-0., -0., 0.], [-0., -0., 0.],
                     [0., -0., -0.], [-0., 0., -0.]])
    np.testing.assert_allclose(forces, test)
    forces = xml_parser.get_forces('initial')
    np.testing.assert_allclose(forces, test)
    forces = xml_parser.get_forces('all')
    np.testing.assert_allclose(forces[1], test)


@pytest.mark.parametrize('xml_parser', ['basic.xml'], indirect=True)
def test_xml_stress(xml_parser):
    """Check stress.

    """

    stress = xml_parser.get_stress('initial')
    test = np.array([[-1.95307089, -0., 0.], [-0., -1.95307089, -0.], [0., -0., -1.95307089]])
    np.testing.assert_allclose(stress, test)
    stress = xml_parser.get_stress('last')
    np.testing.assert_allclose(stress, test)
    stress = xml_parser.get_stress('all')
    np.testing.assert_allclose(stress[1], test)


@pytest.mark.parametrize('xml_parser', ['basic.xml'], indirect=True)
def test_xml_hessian_basic(xml_parser):
    """Check hessian matrix.

    """

    assert xml_parser.get_hessian() == None


@pytest.mark.parametrize('xml_parser', ['basic.xml'], indirect=True)
def test_xml_dynmat_basic(xml_parser):
    """Check the dynamical metrix.

    """

    assert xml_parser.get_dynmat() == None


@pytest.mark.parametrize('xml_parser', ['basic.xml'], indirect=True)
def test_xml_dielectrics_basic(xml_parser):
    """Check the dielectric functions.

    """

    assert xml_parser.get_dielectrics() == None


@pytest.mark.parametrize('xml_parser', ['basic.xml'], indirect=True)
def test_xml_born_basic(xml_parser):
    """Check the born effective masses.

    """

    assert xml_parser.get_born() == None


@pytest.mark.parametrize('xml_parser', ['basic.xml'], indirect=True)
def test_xml_fermi_level(xml_parser):
    """Check the Fermi level.

    """

    assert xml_parser.get_fermi_level() == 5.92134456


@pytest.mark.parametrize('xml_parser', ['basic.xml'], indirect=True)
def test_xml_unitcell(xml_parser):
    """Check the unitcell.

    """

    unitcell = xml_parser.get_unitcell('initial')
    test = np.array([[5.46900498, 0., 0.], [0., 5.46900498, 0.], [0., 0., 5.46900498]])
    np.testing.assert_allclose(unitcell, test)
    unitcell = xml_parser.get_unitcell('last')
    np.testing.assert_allclose(unitcell, test)
    unitcell = xml_parser.get_unitcell('all')
    np.testing.assert_allclose(unitcell[1], test)


@pytest.mark.parametrize('xml_parser', ['basic.xml'], indirect=True)
def test_xml_positions(xml_parser):
    """Check the positions.

    """

    positions = xml_parser.get_positions('initial')
    test = np.array([[0., 0., 0.], [0., 0.50000092, 0.50000092], [0.50000092, 0.50000092, 0.],
                     [0.50000092, 0., 0.50000092], [0.75000046, 0.24999954, 0.75000046],
                     [0.24999954, 0.24999954, 0.24999954], [0.24999954, 0.75000046, 0.75000046],
                     [0.75000046, 0.75000046, 0.24999954]])
    np.testing.assert_allclose(positions, test)
    positions = xml_parser.get_positions('last')
    np.testing.assert_allclose(positions, test)
    positions = xml_parser.get_positions('all')
    np.testing.assert_allclose(positions[1], test)


@pytest.mark.parametrize('xml_parser', ['basic.xml'], indirect=True)
def test_xml_kpoints(xml_parser):
    """Check the kpoints.

    """

    kpoints = xml_parser.get_kpoints()
    test = np.array([[0., 0., 0.], [0.16666667, 0., 0.], [0.33333333, 0., 0.], [0.5, 0., 0.],
                     [0.16666667, 0.16666667, 0.], [0.33333333, 0.16666667, 0.], [0.5, 0.16666667, 0.],
                     [0.33333333, 0.33333333, 0.], [0.5, 0.33333333, 0.], [0.5, 0.5, 0.],
                     [0.16666667, 0.16666667, 0.16666667], [0.33333333, 0.16666667, 0.16666667],
                     [0.5, 0.16666667, 0.16666667], [0.33333333, 0.33333333, 0.16666667], [0.5, 0.33333333, 0.16666667],
                     [0.5, 0.5, 0.16666667], [0.33333333, 0.33333333, 0.33333333], [0.5, 0.33333333, 0.33333333],
                     [0.5, 0.5, 0.33333333], [0.5, 0.5, 0.5]])
    np.testing.assert_allclose(kpoints, test)


@pytest.mark.parametrize('xml_parser', ['basic.xml'], indirect=True)
def test_xml_kpointsw(xml_parser):
    """Check the kpoint weights.

    """

    kpointsw = xml_parser.get_kpointsw()
    test = np.array([
        0.00462963, 0.02777778, 0.02777778, 0.01388889, 0.05555556, 0.11111111, 0.05555556, 0.05555556, 0.05555556,
        0.01388889, 0.03703704, 0.11111111, 0.05555556, 0.11111111, 0.11111111, 0.02777778, 0.03703704, 0.05555556,
        0.02777778, 0.00462963
    ])
    np.testing.assert_allclose(kpointsw, test)


@pytest.mark.parametrize('xml_parser', ['basic.xml'], indirect=True)
def test_xml_dos(xml_parser):
    """Check the density of states

    """

    dos = xml_parser.get_dos()
    assert dos['total']['partial'] == None
    test = np.array([
        -8.1993, -8.1307, -8.0621, -7.9935, -7.9249, -7.8563, -7.7877, -7.7191, -7.6505, -7.5819, -7.5133, -7.4447,
        -7.376, -7.3074, -7.2388, -7.1702, -7.1016, -7.033, -6.9644, -6.8958, -6.8272, -6.7586, -6.69, -6.6214, -6.5527,
        -6.4841, -6.4155, -6.3469, -6.2783, -6.2097, -6.1411, -6.0725, -6.0039, -5.9353, -5.8667, -5.7981, -5.7294,
        -5.6608, -5.5922, -5.5236, -5.455, -5.3864, -5.3178, -5.2492, -5.1806, -5.112, -5.0434, -4.9747, -4.9061,
        -4.8375, -4.7689, -4.7003, -4.6317, -4.5631, -4.4945, -4.4259, -4.3573, -4.2887, -4.2201, -4.1514, -4.0828,
        -4.0142, -3.9456, -3.877, -3.8084, -3.7398, -3.6712, -3.6026, -3.534, -3.4654, -3.3968, -3.3281, -3.2595,
        -3.1909, -3.1223, -3.0537, -2.9851, -2.9165, -2.8479, -2.7793, -2.7107, -2.6421, -2.5735, -2.5048, -2.4362,
        -2.3676, -2.299, -2.2304, -2.1618, -2.0932, -2.0246, -1.956, -1.8874, -1.8188, -1.7502, -1.6815, -1.6129,
        -1.5443, -1.4757, -1.4071, -1.3385, -1.2699, -1.2013, -1.1327, -1.0641, -0.9955, -0.9269, -0.8582, -0.7896,
        -0.721, -0.6524, -0.5838, -0.5152, -0.4466, -0.378, -0.3094, -0.2408, -0.1722, -0.1036, -0.0349, 0.0337, 0.1023,
        0.1709, 0.2395, 0.3081, 0.3767, 0.4453, 0.5139, 0.5825, 0.6511, 0.7198, 0.7884, 0.857, 0.9256, 0.9942, 1.0628,
        1.1314, 1.2, 1.2686, 1.3372, 1.4058, 1.4744, 1.5431, 1.6117, 1.6803, 1.7489, 1.8175, 1.8861, 1.9547, 2.0233,
        2.0919, 2.1605, 2.2291, 2.2977, 2.3664, 2.435, 2.5036, 2.5722, 2.6408, 2.7094, 2.778, 2.8466, 2.9152, 2.9838,
        3.0524, 3.121, 3.1897, 3.2583, 3.3269, 3.3955, 3.4641, 3.5327, 3.6013, 3.6699, 3.7385, 3.8071, 3.8757, 3.9443,
        4.013, 4.0816, 4.1502, 4.2188, 4.2874, 4.356, 4.4246, 4.4932, 4.5618, 4.6304, 4.699, 4.7676, 4.8363, 4.9049,
        4.9735, 5.0421, 5.1107, 5.1793, 5.2479, 5.3165, 5.3851, 5.4537, 5.5223, 5.591, 5.6596, 5.7282, 5.7968, 5.8654,
        5.934, 6.0026, 6.0712, 6.1398, 6.2084, 6.277, 6.3456, 6.4143, 6.4829, 6.5515, 6.6201, 6.6887, 6.7573, 6.8259,
        6.8945, 6.9631, 7.0317, 7.1003, 7.1689, 7.2376, 7.3062, 7.3748, 7.4434, 7.512, 7.5806, 7.6492, 7.7178, 7.7864,
        7.855, 7.9236, 7.9922, 8.0609, 8.1295, 8.1981, 8.2667, 8.3353, 8.4039, 8.4725, 8.5411, 8.6097, 8.6783, 8.7469,
        8.8155, 8.8842, 8.9528, 9.0214, 9.09, 9.1586, 9.2272, 9.2958, 9.3644, 9.433, 9.5016, 9.5702, 9.6388, 9.7075,
        9.7761, 9.8447, 9.9133, 9.9819, 10.0505, 10.1191, 10.1877, 10.2563, 10.3249, 10.3935, 10.4621, 10.5308, 10.5994,
        10.668, 10.7366, 10.8052, 10.8738, 10.9424, 11.011, 11.0796, 11.1482, 11.2168, 11.2855, 11.3541, 11.4227,
        11.4913, 11.5599, 11.6285, 11.6971, 11.7657, 11.8343, 11.9029, 11.9715, 12.0401, 12.1088, 12.1774, 12.246,
        12.3146, 12.3832
    ])
    np.testing.assert_allclose(dos['total']['energy'], test)
    test = np.array([
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 2.00000000e-04, 1.00000000e-03, 3.70000000e-03, 1.19000000e-02, 3.26000000e-02,
        7.62000000e-02, 1.53300000e-01, 2.66500000e-01, 4.03000000e-01, 5.35100000e-01, 6.36900000e-01, 7.08700000e-01,
        7.85700000e-01, 9.11300000e-01, 1.08720000e+00, 1.25030000e+00, 1.31500000e+00, 1.25610000e+00, 1.15020000e+00,
        1.12150000e+00, 1.23750000e+00, 1.45800000e+00, 1.68130000e+00, 1.82360000e+00, 1.86180000e+00, 1.83370000e+00,
        1.81920000e+00, 1.88660000e+00, 2.01500000e+00, 2.08500000e+00, 2.00140000e+00, 1.82570000e+00, 1.74490000e+00,
        1.90040000e+00, 2.27240000e+00, 2.71870000e+00, 3.09640000e+00, 3.35090000e+00, 3.50170000e+00, 3.55490000e+00,
        3.47540000e+00, 3.26920000e+00, 3.03930000e+00, 2.90000000e+00, 2.84830000e+00, 2.76630000e+00, 2.58130000e+00,
        2.40160000e+00, 2.43990000e+00, 2.79200000e+00, 3.32570000e+00, 3.77330000e+00, 3.88710000e+00, 3.55760000e+00,
        2.88190000e+00, 2.11760000e+00, 1.50290000e+00, 1.11840000e+00, 9.21700000e-01, 8.49300000e-01, 8.46700000e-01,
        8.61700000e-01, 8.76100000e-01, 9.33100000e-01, 1.09690000e+00, 1.37400000e+00, 1.67100000e+00, 1.83580000e+00,
        1.76320000e+00, 1.47700000e+00, 1.11540000e+00, 8.34900000e-01, 7.11800000e-01, 7.10700000e-01, 7.45800000e-01,
        7.96500000e-01, 9.71500000e-01, 1.44190000e+00, 2.29450000e+00, 3.42890000e+00, 4.58890000e+00, 5.49890000e+00,
        5.97930000e+00, 5.94670000e+00, 5.37640000e+00, 4.36070000e+00, 3.18920000e+00, 2.25920000e+00, 1.84460000e+00,
        1.95070000e+00, 2.34570000e+00, 2.68260000e+00, 2.67100000e+00, 2.25980000e+00, 1.67430000e+00, 1.22390000e+00,
        1.06650000e+00, 1.15830000e+00, 1.37540000e+00, 1.63440000e+00, 1.91430000e+00, 2.19620000e+00, 2.39300000e+00,
        2.36200000e+00, 2.03010000e+00, 1.49410000e+00, 9.60800000e-01, 5.99100000e-01, 4.64200000e-01, 5.15700000e-01,
        6.66900000e-01, 8.43600000e-01, 1.03810000e+00, 1.29180000e+00, 1.60700000e+00, 1.91400000e+00, 2.15740000e+00,
        2.37420000e+00, 2.64830000e+00, 3.02720000e+00, 3.50900000e+00, 4.04410000e+00, 4.51900000e+00, 4.81470000e+00,
        4.93020000e+00, 4.97960000e+00, 5.01360000e+00, 4.89860000e+00, 4.46000000e+00, 3.75920000e+00, 3.16290000e+00,
        3.08690000e+00, 3.65280000e+00, 4.57020000e+00, 5.35200000e+00, 5.68840000e+00, 5.66130000e+00, 5.59710000e+00,
        5.71520000e+00, 5.94880000e+00, 6.09540000e+00, 6.06380000e+00, 5.92750000e+00, 5.78550000e+00, 5.64500000e+00,
        5.46680000e+00, 5.29570000e+00, 5.26820000e+00, 5.44690000e+00, 5.69100000e+00, 5.76270000e+00, 5.57350000e+00,
        5.28470000e+00, 5.12680000e+00, 5.12890000e+00, 5.08210000e+00, 4.81390000e+00, 4.45130000e+00, 4.31180000e+00,
        4.51220000e+00, 4.78220000e+00, 4.72960000e+00, 4.23110000e+00, 3.50290000e+00, 2.84680000e+00, 2.41840000e+00,
        2.21460000e+00, 2.16660000e+00, 2.17960000e+00, 2.14590000e+00, 1.99870000e+00, 1.75130000e+00, 1.45580000e+00,
        1.14860000e+00, 8.60700000e-01, 6.38300000e-01, 5.09900000e-01, 4.47500000e-01, 3.91300000e-01, 3.06400000e-01,
        2.03600000e-01, 1.13100000e-01, 5.42000000e-02, 2.92000000e-02, 3.50000000e-02, 7.23000000e-02, 1.43700000e-01,
        2.44300000e-01, 3.56000000e-01, 4.55500000e-01, 5.35200000e-01, 6.21200000e-01, 7.62600000e-01, 9.93400000e-01,
        1.30280000e+00, 1.64760000e+00, 1.98840000e+00, 2.30080000e+00, 2.54850000e+00, 2.67450000e+00, 2.66650000e+00,
        2.64030000e+00, 2.79970000e+00, 3.25640000e+00, 3.89990000e+00, 4.48340000e+00, 4.82030000e+00, 4.86440000e+00,
        4.66380000e+00, 4.34560000e+00, 4.12960000e+00, 4.23310000e+00, 4.70730000e+00, 5.41200000e+00, 6.15010000e+00,
        6.76480000e+00, 7.11360000e+00, 7.04970000e+00, 6.50410000e+00, 5.57560000e+00, 4.51990000e+00, 3.66330000e+00,
        3.30350000e+00, 3.59760000e+00, 4.47220000e+00, 5.65180000e+00, 6.79760000e+00, 7.62130000e+00, 7.91420000e+00,
        7.58950000e+00, 6.76810000e+00, 5.76700000e+00, 4.89630000e+00, 4.24300000e+00, 3.72560000e+00, 3.35120000e+00,
        3.28510000e+00, 3.60820000e+00, 4.11010000e+00, 4.41110000e+00, 4.26080000e+00, 3.69330000e+00, 2.94340000e+00,
        2.26050000e+00, 1.77790000e+00, 1.49060000e+00, 1.31000000e+00, 1.13530000e+00, 9.10200000e-01, 6.44600000e-01,
        3.91600000e-01, 2.00100000e-01, 8.49000000e-02, 2.96000000e-02, 8.40000000e-03, 1.90000000e-03, 4.00000000e-04,
        1.00000000e-04, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00
    ])
    np.testing.assert_allclose(dos['total']['total'], test)


@pytest.mark.parametrize('xml_parser', ['basic.xml'], indirect=True)
def test_xml_eigenvalues(xml_parser):
    """Check the egenvalues.

    """

    eigenvalues = xml_parser.get_eigenvalues()
    assert eigenvalues['total'].shape == (24, 20)
    test = np.array([
        -6.19930000e+00, -6.08000000e+00, -5.72390000e+00, -5.13700000e+00, -5.96180000e+00, -5.60910000e+00,
        -5.02880000e+00, -5.26760000e+00, -4.70930000e+00, -4.19570000e+00, -5.84480000e+00, -5.49620000e+00,
        -4.92420000e+00, -5.16110000e+00, -4.61770000e+00, -4.13610000e+00, -4.84950000e+00, -4.35970000e+00,
        -4.00030000e+00, -3.92150000e+00
    ])
    np.testing.assert_allclose(eigenvalues['total'][0], test)
    test = np.array([
        8.18540000e+00, 8.75310000e+00, 9.84280000e+00, 9.91380000e+00, 8.48940000e+00, 9.75230000e+00, 1.00910000e+01,
        9.44600000e+00, 1.02673000e+01, 1.03832000e+01, 8.82250000e+00, 9.92790000e+00, 9.63680000e+00, 9.81580000e+00,
        9.36060000e+00, 9.72520000e+00, 9.69530000e+00, 8.89970000e+00, 9.02760000e+00, 8.98830000e+00
    ])
    np.testing.assert_allclose(eigenvalues['total'][23], test)


@pytest.mark.parametrize('xml_parser', ['gw.xml'], indirect=True)
def test_xml_eigenvalues_gw(xml_parser):
    """Check the egenvalues for GW, which should be corrected.

    """

    eigenvalues = xml_parser.get_eigenvalues()
    assert eigenvalues['total'].shape == (128, 16)
    test = np.array([
        -6.6574, -6.3106, -5.3166, -4.3759, -6.1914, -5.3916, -4.2175, -4.5992, -5.7355, -4.7949, -3.6399, -3.4472,
        -2.5634, -4.4155, -3.4381, -2.4466
    ])
    np.testing.assert_allclose(eigenvalues['total'][0], test)
    test = np.array([
        5.2533, 4.7998, 4.2211, 4.0084, 4.0428, 3.4609, 3.4213, 3.9127, 4.6678, 2.769, 2.625, 3.077, 2.3189, 2.9065,
        2.4315, 1.5386
    ])
    np.testing.assert_allclose(eigenvalues['total'][3], test)


@pytest.mark.parametrize('xml_parser', ['velocities.xml'], indirect=True)
def test_xml_eigenvelocities(xml_parser):
    """Check the egenvelocities.

    """

    eigenvelocities = xml_parser.get_eigenvelocities()
    kpoints = xml_parser.get_kpoints_specific()
    kpointsw = xml_parser.get_kpointsw_specific()
    assert eigenvelocities['total'].shape == (20, 10, 4)
    assert kpoints.shape == (10, 3)
    assert kpointsw.shape == (10,)
    test = np.array([[-6.07600e+00, 0.00000e+00, 0.00000e+00, 0.00000e+00],
                     [-6.05780e+00, 2.82600e-01, -2.82600e-01, 2.82600e-01],
                     [-6.00310e+00, 5.63900e-01, -5.63900e-01, 5.63900e-01],
                     [-5.91220e+00, 8.41300e-01, -8.41300e-01, 8.41300e-01],
                     [-5.78580e+00, 1.11350e+00, -1.11350e+00, 1.11350e+00],
                     [-5.62460e+00, 1.37730e+00, -1.37730e+00, 1.37730e+00],
                     [-5.43020e+00, 1.62690e+00, -1.62690e+00, 1.62690e+00],
                     [-5.20480e+00, 1.85610e+00, -1.85610e+00, 1.85610e+00],
                     [-4.95170e+00, 2.05120e+00, -2.05120e+00, 2.05120e+00],
                     [-4.67680e+00, 2.18960e+00, -2.18960e+00, 2.18960e+00]])
    np.testing.assert_allclose(eigenvelocities['total'][0], test)
    test = np.array([[8.60150e+00, -0.00000e+00, -0.00000e+00, -0.00000e+00],
                     [8.64780e+00, 1.12470e+00, 1.44300e-01, 1.12620e+00],
                     [8.67860e+00, -1.58400e-01, 1.58300e-01, -1.58400e-01],
                     [8.61650e+00, -7.42900e-01, 7.42900e-01, -7.42900e-01],
                     [8.50010e+00, -1.01760e+00, 1.01770e+00, -1.01760e+00],
                     [8.36380e+00, -1.11280e+00, 1.11290e+00, -1.11280e+00],
                     [8.22020e+00, -1.09640e+00, 1.09650e+00, -1.09640e+00],
                     [8.08310e+00, -1.01650e+00, 1.01660e+00, -1.01650e+00],
                     [7.95850e+00, -9.00300e-01, 9.00400e-01, -9.00300e-01],
                     [7.85110e+00, -7.57400e-01, 7.57400e-01, -7.57400e-01]])
    np.testing.assert_allclose(eigenvelocities['total'][4], test)
    test = np.array([[0., 0., 0.], [0.03703704, 0., 0.], [0.07407407, 0., 0.], [0.11111111, -0., -0.],
                     [0.14814815, -0., 0.], [0.18518519, 0., 0.], [0.22222222, -0., -0.], [0.25925926, 0., 0.],
                     [0.2962963, -0., 0.], [0.33333333, -0., -0.]])
    np.testing.assert_allclose(kpoints, test)
    test = np.array([
        5.081e-05, 5.081e-05, 5.081e-05, 5.081e-05, 5.081e-05, 5.081e-05, 5.081e-05, 5.081e-05, 5.081e-05, 5.081e-05
    ])
    np.testing.assert_allclose(kpointsw, test)


@pytest.mark.parametrize('xml_parser', ['specific.xml'], indirect=True)
def test_xml_eigenvalues_specific(xml_parser):
    """Check the egenvalues on specific k-point grids.

    """

    eigenvalues = xml_parser.get_eigenvalues_specific()
    kpoints = xml_parser.get_kpoints_specific()
    kpointsw = xml_parser.get_kpointsw_specific()
    assert eigenvalues['total'].shape == (20, 10)
    assert kpoints.shape == (10, 3)
    assert kpointsw.shape == (10,)
    test = np.array([-6.076, -6.0578, -6.0031, -5.9122, -5.7858, -5.6246, -5.4302, -5.2048, -4.9517, -4.6768])
    np.testing.assert_allclose(eigenvalues['total'][0], test)
    test = np.array([9.5694, 9.6943, 10.0793, 10.646, 11.2894, 11.9561, 12.6122, 13.2292, 13.6978, 13.9563])
    np.testing.assert_allclose(eigenvalues['total'][7], test)
    test = np.array([[0., 0., 0.], [0.03703704, 0., 0.], [0.07407407, 0., -0.], [0.11111111, 0., -0.],
                     [0.14814815, 0., -0.], [0.18518519, -0., 0.], [0.22222222, -0., 0.], [0.25925926, -0., 0.],
                     [0.2962963, -0., -0.], [0.33333333, -0., -0.]])
    np.testing.assert_allclose(kpoints, test)
    test = np.array([
        5.0810e-05, 4.0644e-04, 4.0644e-04, 4.0644e-04, 4.0644e-04, 4.0644e-04, 4.0644e-04, 4.0644e-04, 4.0644e-04,
        4.0644e-04
    ])
    np.testing.assert_allclose(kpointsw, test)


@pytest.mark.parametrize('xml_parser', ['basic.xml'], indirect=True)
def test_xml_occupancies(xml_parser):
    """Check the occupancies.

    """

    occupancies = xml_parser.get_occupancies()['total']
    assert occupancies.shape == (24, 20)
    test = np.array([
        1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00,
        1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00,
        1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00
    ])
    np.testing.assert_allclose(occupancies[0], test)
    test = np.array([
        9.81500000e-01, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 9.98300000e-01, 1.00000000e+00, 1.00000000e+00,
        1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00,
        1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00
    ])
    np.testing.assert_allclose(occupancies[15], test)


@pytest.mark.parametrize('xml_parser', ['basicspin.xml'], indirect=True)
def test_xml_dos_spin(xml_parser):
    """Check the density of states for spin resolved.

    """

    dos = xml_parser.get_dos()
    assert dos['down']['partial'] == None
    assert dos['up']['partial'] == None
    test = np.array([-10., -9.98, -9.96, -9.9399, -9.9199])
    np.testing.assert_allclose(dos['total']['energy'][0:5], test)
    test = np.array([9.9199, 9.9399, 9.96, 9.98, 10.])
    np.testing.assert_allclose(dos['total']['energy'][995:1000], test)
    test = np.array([1.7104, 1.6289, 1.5543, 1.4882, 1.4315, 1.3845, 1.3467, 1.3172, 1.2945, 1.2772])
    np.testing.assert_allclose(dos['down']['total'][460:470], test)
    test = np.array([1.708, 1.6267, 1.5523, 1.4864, 1.43, 1.3833, 1.3457, 1.3164, 1.294, 1.2767])

    np.testing.assert_allclose(dos['up']['total'][460:470], test)


@pytest.mark.parametrize('xml_parser', ['basicspin.xml'], indirect=True)
def test_xml_eigenvalues_spin(xml_parser):
    """Check the egenvalues for spin resolved.

    """

    eigenvalues = xml_parser.get_eigenvalues()
    test = np.array([-6.2357, -6.1505, -5.8992])
    np.testing.assert_allclose(eigenvalues['down'][0, 0:3], test)
    test = np.array([8.2369, 8.5213, 9.536])
    np.testing.assert_allclose(eigenvalues['down'][23, 0:3], test)
    test = np.array([
        -6.2363,
        -6.1511,
        -5.8998,
    ])
    np.testing.assert_allclose(eigenvalues['up'][0, 0:3], test)
    test = np.array([8.2371, 8.5208, 9.5273])
    np.testing.assert_allclose(eigenvalues['up'][23, 0:3], test)


@pytest.mark.parametrize('xml_parser', ['basicpartial.xml'], indirect=True)
def test_xml_dos_partial(xml_parser):
    """Check the decomposed density of states.

    """

    dos = xml_parser.get_dos()
    assert dos['total']['partial'].shape == (8, 1000, 9)
    test = np.array([0.1287, 0.1216, 0.1152, 0.1095, 0.1046, 0.1005, 0.0973, 0.0947, 0.0927, 0.0912])
    np.testing.assert_allclose(dos['total']['partial'][0, 460:470, 0], test)
    test = np.array([0.1429, 0.1345, 0.1268, 0.1201, 0.1144, 0.1097, 0.1059, 0.1031, 0.101, 0.0995])
    np.testing.assert_allclose(dos['total']['partial'][7, 460:470, 0], test)


@pytest.mark.parametrize('xml_parser', ['basicpartial.xml'], indirect=True)
def test_xml_eivenalues_partial(xml_parser):
    """Check the decomposed eigenvalues.

    """

    eigenvalues = xml_parser.get_eigenvalues()
    assert eigenvalues['total'].shape == (21, 64)
    projected = xml_parser.get_projectors()
    assert projected['total'].shape == (8, 21, 64, 9)
    test = np.array([0.0518, 0.0507, 0.0521])
    np.testing.assert_allclose(projected['total'][0, 0, 2:5, 0], test)
    test = np.array([0., 0., 0.0002])
    np.testing.assert_allclose(projected['total'][0, 0, 2:5, 1], test)
    test = np.array([0.025, 0.0001, 0.0243])
    np.testing.assert_allclose(projected['total'][4, 10, 2:5, 1], test)


@pytest.mark.parametrize('xml_parser', ['basicpartial.xml'], indirect=True)
def test_xml_parameters_partial(xml_parser):
    """Check the parsing of parameters"""
    parameters = xml_parser.get_parameters()
    assert parameters['nelm'] == 60
    assert parameters['nsw'] == 0
    assert parameters['nbands'] == 21
    assert parameters['ispin'] == 1


@pytest.mark.parametrize('xml_parser', ['basic.xml'], indirect=True)
def test_xml_version(xml_parser):
    """Check the parsing of the version"""
    version = xml_parser.get_version()
    assert version == '5.4.1'


@pytest.mark.parametrize('xml_parser', ['dielectrics.xml'], indirect=True)
def test_xml_dielectrics(xml_parser):
    """Check the dielectric function.

    """

    dielectrics = xml_parser.get_dielectrics()
    assert dielectrics['real'].shape == (1000, 6)
    assert dielectrics['imag'].shape == (1000, 6)
    assert dielectrics['energy'].shape == (1000,)
    test = np.array([1.20757000e+01, 1.14969000e+01, 1.14969000e+01, 0.00000000e+00])
    np.testing.assert_allclose(dielectrics['real'][0, 0:4], test)
    test = np.array([-0.6195, -0.6116, -0.6037, -0.5957, -0.5876])
    np.testing.assert_allclose(dielectrics['real'][490:495, 1], test)
    test = np.array([0.1129, 0.1167, 0.1167, 0.])
    np.testing.assert_allclose(dielectrics['imag'][550, 0:4], test)
    test = np.array([0.1082, 0.1066, 0.105, 0.1034, 0.1017])
    np.testing.assert_allclose(dielectrics['imag'][490:495, 1], test)
    test = np.array([10.0875, 10.1081, 10.1286, 10.1492, 10.1698])
    np.testing.assert_allclose(dielectrics['energy'][490:495], test)


@pytest.mark.parametrize('xml_parser', ['disp.xml'], indirect=True)
def test_xml_dynmat(xml_parser):
    """Check the dynamical matrix from displacements.

    """

    dynmat = xml_parser.get_dynmat()
    assert dynmat['eigenvectors'].shape == (24, 24)
    assert dynmat['eigenvalues'].shape == (24,)
    test = np.array([-5.16257351e-01, 8.16789156e-17, 8.95098005e-02])
    np.testing.assert_allclose(dynmat['eigenvectors'][0, 8:11], test)
    test = np.array([-4.90209923e-02, -2.33058348e-01, -2.33058348e-01])
    np.testing.assert_allclose(dynmat['eigenvectors'][10, 12:15], test)
    test = np.array([-0.73230558, -0.73016562, -0.72285018])
    np.testing.assert_allclose(dynmat['eigenvalues'][5:8], test)


@pytest.mark.parametrize('xml_parser', ['disp.xml'], indirect=True)
def test_xml_hessian(xml_parser):
    """Check the hessian from displacements.

    """

    hessian = xml_parser.get_hessian()
    assert hessian.shape == (24, 24)
    test = np.array([-0.46355041, 0., 0., -0.05917741])
    np.testing.assert_allclose(hessian[0][0:4], test)
    test = np.array([0.11487952, 0.08151255, 0.08370068, 0.11487952])
    np.testing.assert_allclose(hessian[15][0:4], test)
    test = np.array([0.11431486, -0.0818301])
    np.testing.assert_allclose(hessian[15][9:11], test)


@pytest.mark.parametrize('xml_parser', ['localfield.xml'], indirect=True)
def test_xml_born(xml_parser):
    """Check the hessian from displacements.

    """

    born = xml_parser.get_born()
    assert born.shape == (8, 3, 3)
    test = np.array([[0.00637225, 0., 0.], [-0.00064313, -0.20498926, 0.05499278],
                     [-0.00042176, -0.21957021, 0.03207096]])
    np.testing.assert_allclose(born[0], test)
    test = np.array([[0.10926701, 0.04003354, -0.04003354], [-0.01047578, 0.13487262, 0.02706512],
                     [0.01046009, 0.0280611, 0.13400096]])
    np.testing.assert_allclose(born[5], test)


@pytest.mark.parametrize('xml_parser', ['magmom.xml'], indirect=True)
def test_xml_structure_magmom(xml_parser):
    """Check the unitcell and positions for a magmom xml file.

    """

    unitcell_initial = xml_parser.get_unitcell('initial')
    test = np.array([[0., 3.2395, 3.2395], [3.2395, 0., 3.2395], [3.2395, 3.2395, 0.]])
    np.testing.assert_allclose(unitcell_initial, test)
    unitcell_last = xml_parser.get_unitcell('last')
    np.testing.assert_allclose(unitcell_last, unitcell_initial)
    unitcell_all = xml_parser.get_unitcell('all')
    np.testing.assert_allclose(unitcell_all[1], unitcell_initial)

    positions_initial = xml_parser.get_positions('initial')
    test = np.array([[0., 0., 0.], [0.25, 0.25, 0.25]])
    np.testing.assert_allclose(positions_initial, test)
    positions_last = xml_parser.get_positions('last')
    np.testing.assert_allclose(positions_last, positions_initial)
    positions_all = xml_parser.get_positions('all')
    np.testing.assert_allclose(positions_all[1], positions_initial)


@pytest.mark.parametrize('xml_parser', ['basicrelax.xml'], indirect=True)
def test_xml_ionic(xml_parser):
    """Check the unitcell, positions, forces and stress for multiple ionic steps.

    """

    unitcells = xml_parser.get_unitcell('all')
    positions = xml_parser.get_positions('all')
    forces = xml_parser.get_forces('all')
    stress = xml_parser.get_stress('all')
    energies_sc = xml_parser.get_energies('all', nosc=False)

    # check that all entries are present
    assert len(unitcells) == 19
    assert len(positions) == 19
    assert len(forces) == 19
    assert len(stress) == 19

    # check some random entries
    testing = np.array([0.00000000e+00, 5.46644175e+00, 4.10279000e-03])
    np.testing.assert_allclose(unitcells[8][1], testing)
    testing = np.array([0.00000000e+00, 8.30440000e-04, 5.46738152e+00])
    np.testing.assert_allclose(unitcells[15][2], testing)
    testing = np.array([-0.00630478, 0.5, 0.5])
    np.testing.assert_allclose(positions[6][1], testing)
    testing = np.array([0.24381576, 0.75131665, 0.74868335])
    np.testing.assert_allclose(positions[14][6], testing)
    testing = np.array([-0.69286285, 0.0, 0.0])
    np.testing.assert_allclose(forces[2][1], testing)
    testing = np.array([0.00344071, -0.0331652, -0.0331652])
    np.testing.assert_allclose(forces[11][4], testing)
    testing = np.array([-6.18541234, 0.0, 0.0])
    np.testing.assert_allclose(stress[2][0], testing)
    testing = np.array([0.0, 0.60834449, -3.20314152])
    np.testing.assert_allclose(stress[10][1], testing)
