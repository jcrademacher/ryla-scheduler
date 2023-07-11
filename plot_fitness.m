fname = "fitnesses/fitness_pop500_ep10_mp50_i1000_07m-10d-23y_11H-34M-52S.bin";
fid = fopen(fname,"r");

fitness = fread(fid,'uint32');
hold on;
plot(fitness);
xlabel("Generation");
ylabel("Fitness")