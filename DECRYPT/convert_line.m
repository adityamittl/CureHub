function output_data = convert_line(input_data)
%CureHub
sz = size(input_data);

output_data = reshape(input_data,[1 sz(1)*sz(2)]);
for (ii=1:length(output_data))
    if(output_data(ii) == 124)
        output_data = output_data(1:ii-1);
        break
    end
end

end
