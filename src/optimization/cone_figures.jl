
using Plots
using LinearAlgebra
using DelimitedFiles

M_spotify_alpha = readdlm("./outputs/optimization/spotify_estimator_alpha.txt")

features_spotify = readdlm("./features/txt/features.txt")

println(size(M_spotify_alpha))

println(size(features_spotify[1, :]))

x_axis = 1
y_axis = 18

# Procesamiento del Alpha

a = 1.5141161212919718e-6
b = 1.7208871806760954e-7

f = features_spotify[y_axis, :]

x = range(-1, stop = 1, length = 100)
y = range(-1, stop = 1, length = 100)

z = ((a^2) * (x.^2)+(b^2) * (y.^2)).^(1/2)

plotd = plot(x, z)

ylims!((-10, 100))
scatter!(f, [i for i=1:100])

savefig(plotd, string("./outputs/cone_plot_alpha_", x_axis, "_", y_axis, ".png"))
