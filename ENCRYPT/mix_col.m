function output_data = mix_col(input_data,key)

%KEY MUST BE >= 4 char

data_size = size(input_data);
tmp = key;
% str_key = num2str(key)
% len_str = length(str_key)
poly_key = [];


while (length(poly_key) < data_size(2))
    while(tmp >1)
        poly_key(1,length(poly_key)+1) = mod(tmp,10);
        tmp = tmp / 10;
    end
    if (length(poly_key) < data_size(2))
        tmp = key;
    end
end
        
poly_key = fix(poly_key); %Rounds down decimals to nearest whole digit
poly_key = poly_key(1,1:data_size)';
input_data;
for(ii = 1:data_size(2))
    output_data(:,ii) = input_data(:,ii).*poly_key;
end

end
