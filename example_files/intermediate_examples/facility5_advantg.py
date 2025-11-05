from advantg.driver import run

inp = {
    "method":                    "cadis",
    "mcnp_input":                "facility5_advantg.txt",
    "mcnp_tallies":              [ 4 ],
    "silo_ww":                   True,
    "anisn_library":             "27n19g",
    "denovo_x_blocks":           3,
    "denovo_y_blocks":           2,
    "denovo_z_blocks":           1,
    "denovo_pn_order":           1,
    "denovo_quad_num_polar":     4,
    "denovo_quad_num_azi":       4,
    "mcnp_min_rays_per_face":  250,
    "mesh_x":                    [ -750, -700, -100, -50,  50, 100, 700, 750 ],
    "mesh_x_ints":               [         10,   20,  10,  20,  10,  20,  10 ],
    "mesh_y":                    [ -350, -300, -200, 200, 300, 350 ],
    "mesh_y_ints":               [         10,   10,  20,  10,  10 ],
    "mesh_z":                    [  -50,    0,  250, 300, 310 ],
    "mesh_z_ints":               [         10,   10,  10,   1 ]
}

run(inp)
