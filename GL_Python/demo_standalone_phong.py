import argparse
from shapes import make_shapes_dict, make_sphere, make_torus, make_cone

def main():
    parser = argparse.ArgumentParser(
        description="Phong-shaded shape renderer with Z-buffer. "
                    "Supports cube, tetrahedron, cone, sphere, torus."
    )
    parser.add_argument("--shape", choices=["cube", "tetrahedron", "cone", "sphere", "torus"],
                        default="sphere", help="Which shape to render (default: sphere)")
    parser.add_argument("--frames", type=int, default=60,
                        help="Number of frames to render for animation (default: 60)")
    parser.add_argument("--gif", help="Output GIF file")
    parser.add_argument("--png-dir", help="Directory for per-frame PNGs")
    parser.add_argument("--size", default="256x256",
                        help="Image resolution WxH (default: 256x256)")

    # Lighting
    parser.add_argument("--ambient", type=float, default=0.2,
                        help="Ambient light intensity (default: 0.2)")
    parser.add_argument("--light", nargs="+", action="append",
                        help="Directional light: dx dy dz [color] (repeatable)")
    parser.add_argument("--point", nargs="+", action="append",
                        help="Point light: px py pz [color] (repeatable)")
    parser.add_argument("--specular", type=float, default=0.5,
                        help="Specular reflection coefficient (default: 0.5)")
    parser.add_argument("--shininess", type=int, default=32,
                        help="Phong shininess exponent (default: 32)")

    # Shape-specific params with defaults documented
    parser.add_argument("--radius", type=float,
                        help="Radius (sphere default=1.0, torus minor=0.3, cone base=1.0)")
    parser.add_argument("--height", type=float,
                        help="Cone height (default=2.0)")
    parser.add_argument("--R", type=float,
                        help="Torus major radius (default=1.0)")
    parser.add_argument("--r", type=float,
                        help="Torus minor radius (default=0.3)")
    parser.add_argument("--n_lat", type=int,
                        help="Sphere latitude subdivisions (default=16)")
    parser.add_argument("--n_lon", type=int,
                        help="Sphere longitude subdivisions (default=32)")
    parser.add_argument("--nu", type=int,
                        help="Torus U subdivisions (default=32)")
    parser.add_argument("--nv", type=int,
                        help="Torus V subdivisions (default=16)")

    args = parser.parse_args()

    shapes = make_shapes_dict()
    if args.shape == "sphere":
        polys = make_sphere(
            radius=args.radius or 1.0,
            n_lat=args.n_lat or 16,
            n_lon=args.n_lon or 32
        )
    elif args.shape == "torus":
        polys = make_torus(
            R=args.R or 1.0,
            r=args.r or 0.3,
            nu=args.nu or 32,
            nv=args.nv or 16
        )
    elif args.shape == "cone":
        polys = make_cone(
            radius=args.radius or 1.0,
            height=args.height or 2.0,
            n=32
        )
    else:
        polys = shapes[args.shape]()

    print(f"Generated {len(polys)} polygons for {args.shape}")
    # TODO: feed polys into renderer with args.light/args.point etc.

if __name__ == "__main__":
    main()
