import dwavebinarycsp
from hybrid.reference.kerberos import KerberosSampler

from utilities import visualize_map


class State:
    def __init__(self, name):
        self.name = name
        self.red = name + "_r"
        self.green = name + "_g"
        self.blue = name + "_b"
        self.cyan = name + "_c"
        


# Set up states
ca = State("ca")   # California
az = State("az")   # Arizona
nv = State("nv")   # Nevada
ut = State("ut")   # Utah
ore = State("ore") # Oregon
col = State("col") # Colorado
wa = State("wa")   # Washington
ida = State("ida") # Idaho
mo = State("mo")   # Montana
wy = State("wy")   # Wyoming
nm = State("nm")   # New Mexico
tx = State("tx")   # Texas
ok = State("ok")   # Oklahoma
hi = State("hi")   # Hawaii
ks = State("ks")   # Kansas
ne = State("ne")   # Nebraska
sd = State("sd")   # South Dakota
nd = State("nd")   # North Dakota
ws = State("ws")   # Wisconsin
mn = State("mn")   # Minnesota
iw = State("iw")   # Iowa
ms = State("ms")   # Missouri
ak = State("ak")   # Arkansas
la = State("la")   # Louisiana
mp = State("mp")   # Mississippi
il = State("il")   # Illinois
ind = State("ind") # Indiana
mi = State("mi")   # Michigan
oh = State("oh")   # Ohio
ky = State("ky")   # Kentucky
tn = State("tn")   # Tennessee
al = State("al")   # Alabama
ga = State("ga")   # Georgia
fl = State("fl")   # Florida
sc = State("sc")   # South Carolina
nc = State("nc")   # North Carolina
va = State("va")   # Virginia
wv = State("wv")   # West Virginia
ml = State("ml")   # Maryland
dl = State("dl")   # Delaware
nj = State("nj")   # New Jersey
pn = State("pn")   # Pennsylvania
ny = State("ny")   # New York
cn = State("cn")   # Connecticut
ri = State("ri")   # Rhode Island
ma = State("ma")   # Massachusetts
ve = State("ve")   # Vermont
nh = State("nh")   # New Hampshire
me = State("me")   # Maine
ax = State("ax")   # Alaska

states = [ca, az, nv, ut, ore, col, wa, ida, mo, wy, nm, tx, ok, hi, ks, ne, sd, nd, mn, iw, ms, ak, la, mp, il, ind, mi, oh, ky, tn, al, ga, fl, sc, nc, va, wv, ml, dl, nj, pn, ny, cn, ri, ma, ve, nh, me, ax]


neighbours = [(ca, az ),
              (ca, nv),
              (ca, ore),
              (ore, wa),
              (ore, nv),
              (ore, ida),
              (wa, ida),
              (ida, ut),
              (ida, nv),
              (ida, wy),
              (ida, mo),
              (ida, ore),
              (nv, ut),
              (nv, az),
              (nv, ore),
              (az, ut),
              (az, nm),
              (az, col),
              (ut, col),
              (ut, nm),
              (ut, wy),
              (mo, wy),
              (mo, nd),
              (mo, sd),
              (wy, sd),
              (wy, ne),
              (wy, col),
              (col, nm),
              (col, ne),
              (col, ok),
              (col, ks),
              (nm, tx),
              (nm, ok),
              (tx, ok),
              (tx, la),
              (tx, ak),
              (ok, ks),
              (ok, ms),
              (ok, ak),
              (ks, ne),
              (ks, ms),
              (ne, sd),
              (ne, iw),
              (ne, ms),
              (sd, iw),
              (sd, mn),
              (nd, mn),
              (nd, sd),
              (mn, ws),
              (mn, iw),
              (iw, ws),
              (iw, il),
              (iw, ms),
              (ms, il),
              (ms, ak),
              (ms, ky),
              (ms, tn),
              (ak, tn),
              (ak, mp),
              (ak, la),
              (la, mp),
              (mp, al),
              (mp, tn),
              (tn, ky),
              (tn, va),
              (tn, nc),
              (tn, al),
              (tn, ga),
              (ky, il),
              (ky, ind),
              (ky, oh),
              (ky, wv),
              (ky, va),
              (il, ws),
              (il, ind),
              (ws, mi),
              (mi, ind),
              (mi, oh),
              (ind, oh),
              (oh, pn),
              (oh, wv),
              (al, ga),
              (al, fl),
              (ga, fl),
              (ga, sc),
              (ga, nc),
              (sc, nc),
              (nc, va),
              (va, wv),
              (va, ml),
              (ml, dl),
              (ml, wv),
              (ml, pn),
              (dl, pn),
              (dl, nj),
              (nj, pn),
              (nj, ny),
              (pn, ny),
              (pn, wv),
              (ny, cn),
              (ny, ma),
              (ny, ve),
              (cn, ri),
              (cn, ma),
              (ri, ma),
              (ma, ve),
              (ma, nh),
              (ve, nh),
              (nh, me),
              (wa, ax),
              (ca, hi)]

# Initialize constraint satisfaction problem
csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
not_both = {(0, 1), (1, 0), (0, 0)}
select_one = {(0, 0, 0, 1),
              (0, 0, 1, 0),
              (0, 1, 0, 0),
              (1, 0, 0, 0)}

# Apply one color constraint
for p in states:
    csp.add_constraint(select_one, {p.red, p.green, p.blue, p.cyan})

# Apply no color sharing between neighbours
for x, y in neighbours:
    csp.add_constraint(not_both, {x.red, y.red})
    csp.add_constraint(not_both, {x.green, y.green})
    csp.add_constraint(not_both, {x.blue, y.blue})
    csp.add_constraint(not_both, {x.cyan, y.cyan})


bqm = dwavebinarycsp.stitch(csp)


solution = KerberosSampler().sample(bqm,
                       qpu_params={'label': 'Example - Map Coloring'})
best_solution = solution.first.sample
print("Solution: ", best_solution)

# Verify
is_correct = csp.check(best_solution)
print("Is this correct? {}".format(is_correct))

# make the graph visibile

# node positions for map of US
node_positions = {"ax": (-3, 10),
                  "wa": (0, 5),
                  "ore": (0, 3),
                  "ca": (0, 0),
                  "nv": (1, 2),
                  "ida": (2, 4),
                  "mo": (3, 5),
                  "ut": (2, 2),
                  "az": (2, 0),
                  "wy": (4, 4),
                  "col": (4, 2),
                  "nm": (4, 0),
                  "nd": (6, 5),
                  "sd": (6, 4),
                  "ne": (6, 3),
                  "ks": (6, 2),
                  "ok": (6, 0),
                  "tx": (6, -3),
                  "mn": (8, 5),
                  "iw": (8, 4),
                  "ms": (8, 2),
                  "ak": (8, 0),
                  "la": (8, -2),
                  "ws": (10, 6),
                  "il": (9, 3),
                  "mp": (10, -2),
                  "mi": (11, 5),
                  "ind": (10, 3),
                  "ky": (11, 2),
                  "tn": (11, 0),
                  "al": (11, -2),
                  "oh": (12, 3),
                  "ga": (13, -2),
                  "fl": (14, -4),
                  "ny": (14, 6),
                  "nj": (15, 3),
                  "pn": (13, 4),
                  "wv": (13, 2),
                  "va": (15, 1),
                  "ml": (14, 2),
                  "dl": (15, 2),
                  "nc": (14, 0),
                  "sc": (14, -1),
                  "ve": (16, 7),
                  "ma": (16, 6),
                  "cn": (16, 5),
                  "nh": (17, 7),
                  "ri": (17, 5),
                  "me": (18, 9),
                  "hi": (-3, 1),}

nodes = [u.name for u in states]
edges = [(u.name, v.name) for u, v in neighbours]
visualize_map(nodes, edges, best_solution, node_positions=node_positions)
