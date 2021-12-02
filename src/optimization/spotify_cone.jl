
using DelimitedFiles
using JuMP
using Ipopt
using LinearAlgebra

debug = false

println("Definiendo el problema...")

model = Model(Ipopt.Optimizer)


@variable(model, alpha[1:20] >= 0)

@objective(model, Min, -sum(alpha))

println("Variable y FO definidas...")

m = readdlm("./features/txt/features.txt")
z = 1

for col in eachcol(m)
    global z

    constr1 = sum((alpha[i]*col[i])^2 for i = 1:20)

    if debug
        println(constr)
    end

    @NLconstraint(model, constr1 <= z^2)

    println("Restriccion ", z, " implementada...")
    z = z+1
end


println("Optimizando!...")
optimize!(model)

# Resultados
println("Resultados!...")

println("alpha1: ", JuMP.value(alpha[1]))
println("alpha2: ", JuMP.value(alpha[2]))
println("alpha3: ", JuMP.value(alpha[3]))
println("alpha4: ", JuMP.value(alpha[4]))
println("alpha5: ", JuMP.value(alpha[5]))
println("alpha6: ", JuMP.value(alpha[6]))
println("alpha7: ", JuMP.value(alpha[7]))
println("alpha8: ", JuMP.value(alpha[8]))
println("alpha9: ", JuMP.value(alpha[9]))
println("alpha10: ", JuMP.value(alpha[10]))
println("alpha11: ", JuMP.value(alpha[11]))
println("alpha12: ", JuMP.value(alpha[12]))
println("alpha13: ", JuMP.value(alpha[13]))
println("alpha14: ", JuMP.value(alpha[14]))
println("alpha15: ", JuMP.value(alpha[15]))
println("alpha16: ", JuMP.value(alpha[16]))
println("alpha17: ", JuMP.value(alpha[17]))

open("outputs/optimization/spotify_estimator_alpha_actual.txt", "w") do io
    write(io, string([JuMP.value(alpha[i]) for i = 1:20]))
end;
