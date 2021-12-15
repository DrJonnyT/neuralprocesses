from .lik import construct_likelihood
from ..util import register_model

__all__ = ["create_construct_convgnp"]


@register_model
def create_construct_convgnp(ns):
    def construct_convgnp(
        dim_x=1,
        dim_y=1,
        points_per_unit=64,
        margin=0.1,
        likelihood="het",
        num_basis_functions=64,
        dtype=None,
    ):
        unet_out_channels, likelihood = construct_likelihood(
            ns,
            ns,
            spec=likelihood,
            dim_y=dim_y,
            num_basis_functions=num_basis_functions,
        )
        unet = ns.UNet(
            dim=dim_x,
            in_channels=dim_y + 1,
            out_channels=unet_out_channels,
            dtype=dtype,
        )
        disc = ns.Discretisation(
            points_per_unit=points_per_unit,
            multiple=2 ** unet.num_halving_layers,
            margin=margin,
            dim=dim_x,
        )
        return ns.Model(
            ns.FunctionalCoder(
                disc,
                ns.SetConv(disc.points_per_unit, density_channel=True, dtype=dtype),
            ),
            ns.Chain(unet, ns.SetConv(disc.points_per_unit, dtype=dtype), likelihood),
        )

    return construct_convgnp