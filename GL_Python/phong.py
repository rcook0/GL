def phong_shading(normal, light_dir=(0,0,-1), view_dir=(0,0,-1),
                  ka=0.1, kd=0.7, ks=0.2, shininess=16):
    # Normalize
    n = normal / np.linalg.norm(normal)
    l = np.array(light_dir) / np.linalg.norm(light_dir)
    v = np.array(view_dir) / np.linalg.norm(view_dir)
    r = 2 * np.dot(n, l) * n - l  # reflection
    
    # Components
    ambient = ka
    diffuse = kd * max(np.dot(n, l), 0)
    specular = ks * max(np.dot(r, v), 0) ** shininess
    return ambient + diffuse + specular
