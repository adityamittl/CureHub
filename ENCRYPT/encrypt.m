function final_data = encrypt(input_data,reps,user_key)

%CureHub
input_data = int64(input_data);
if(length(user_key) < 4)
    fprintf('The length of the user key is insufficient. Minimum = 4 char. Current = %s',user_key);
    return
end
if (isempty(input_data))
    fprintf('No data inputted');
    return
end
if (reps < 1)
    fprintf('The number of repetitions is insufficient. Minimum >= 1 reps. Current = %d',reps);
    return
end

crypt_key = gen_key(user_key);
final_data = convert_sq(input_data);
final_data = add_key_to_data(final_data,crypt_key);

for (ii = 1:reps)
    final_data = shift_row(final_data);
    final_data = mix_col(final_data,crypt_key);
    final_data = add_key_to_data(final_data,crypt_key);
end

final_data = shift_row(final_data);
final_data = add_key_to_data(final_data,crypt_key);

end
