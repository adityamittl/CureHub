function crypt_key = gen_key(user_key)
%CureHub
crypt_key = [];
crypt_key = int16(user_key); %CHAR -> ASCII NUMBER
for(ii=1:size(user_key))
    crypt_key = sum(user_key');
end
crypt_key = (crypt_key + 27)/3;
crypt_key = fix(crypt_key);

end
