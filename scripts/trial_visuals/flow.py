"""Streamlines round an aerofoil from potential flow (Joukowski transform), for the Principles of Flight pictures.

A circle in the zeta-plane, offset by mu so that z = zeta + 1/zeta maps it to a cambered aerofoil, carries a uniform
flow at angle of attack alpha plus the circulation the Kutta condition sets (the flow leaves the trailing edge
smoothly). Contours of the stream function are mapped back to the z-plane. Coordinates come out with the free
stream along +x, the aerofoil's leading edge on the left and its chord tilted nose-up by alpha.
"""
import math

import numpy as np

MU = complex(-0.09, 0.07)         # circle centre: thickness (real part) and camber (imaginary part)
RADIUS = abs(1 - MU)              # passes through zeta = 1, which maps to the sharp trailing edge


def _rotate(z, alpha):
    return z * np.exp(-1j * alpha)


def aerofoil_outline(alpha_deg, n=240):
    """Aerofoil outline, free stream along +x (the section is rotated nose-up by alpha)."""
    t = np.linspace(0, 2 * np.pi, n)
    zeta = MU + RADIUS * np.exp(1j * t)
    return _rotate(zeta + 1 / zeta, math.radians(alpha_deg))


def chord_ends(alpha_deg):
    """(leading edge, trailing edge) in the same frame as the outline."""
    z0 = aerofoil_outline(0.0, 1440)
    le, te = z0[np.argmin(z0.real)], z0[np.argmax(z0.real)]
    a = math.radians(alpha_deg)
    return complex(le * np.exp(-1j * a)), complex(te * np.exp(-1j * a))


def body_psi(alpha_deg):
    a = math.radians(alpha_deg)
    gamma = 4 * math.pi * RADIUS * math.sin(a + math.asin(MU.imag / RADIUS))
    return gamma / (2 * math.pi) * math.log(RADIUS), gamma


def streamlines(alpha_deg, offsets, extent=(-3.6, 3.6, -1.9, 1.9)):
    """Streamlines (complex arrays, left to right) at stream-function `offsets` from the one that meets the
    stagnation point (about the height, far upstream, above or below the dividing streamline)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    a = math.radians(alpha_deg)
    psi_body, gamma = body_psi(alpha_deg)
    r = np.geomspace(RADIUS * 1.0005, RADIUS * 12, 900)
    th = np.linspace(0, 2 * np.pi, 1440)
    Rg, Tg = np.meshgrid(r, th)
    zp = Rg * np.exp(1j * Tg)                                 # zeta - mu
    w = np.exp(-1j * a) * zp + RADIUS ** 2 / (np.exp(-1j * a) * zp) + 1j * gamma / (2 * np.pi) * np.log(zp)
    psi = w.imag
    zeta = MU + zp
    z = _rotate(zeta + 1 / zeta, a)                           # stream along +x
    fig = plt.figure()
    cs = plt.contour(np.arange(psi.shape[1]), np.arange(psi.shape[0]), psi, levels=sorted(psi_body + o for o in offsets))
    out = []
    x0, x1, y0, y1 = extent
    for segs in cs.allsegs:
        for seg in segs:
            if len(seg) < 5:
                continue
            fj, fi = seg[:, 0], seg[:, 1]
            j0 = np.clip(np.floor(fj).astype(int), 0, psi.shape[1] - 2)
            i0 = np.clip(np.floor(fi).astype(int), 0, psi.shape[0] - 2)
            dj, di = fj - j0, fi - i0
            pts = (z[i0, j0] * (1 - dj) * (1 - di) + z[i0, j0 + 1] * dj * (1 - di)
                   + z[i0 + 1, j0] * (1 - dj) * di + z[i0 + 1, j0 + 1] * dj * di)
            keep = (pts.real > x0) & (pts.real < x1) & (pts.imag > y0) & (pts.imag < y1)
            pts = pts[keep]
            if len(pts) > 5:
                out.append(pts[np.argsort(pts.real)])
    plt.close(fig)
    return out
