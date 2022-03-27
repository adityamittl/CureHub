function final_data = decrypt(input_data,reps,user_key)
%CureHub
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
final_data = remove_key_from_data(input_data,crypt_key);
final_data = rev_shift_row(final_data);

for (ii = 1:reps)
    final_data = remove_key_from_data(final_data,crypt_key);
    final_data = rev_mix_col(final_data,crypt_key);
    final_data = rev_shift_row(final_data);
end

final_data = remove_key_from_data(final_data,crypt_key);
final_data = convert_line(final_data);
final_data = char(final_data);


end
