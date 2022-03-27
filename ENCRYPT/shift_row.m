function output_data = shift_row(input_data)
%CureHub
input_data
sz = size(input_data);
%Where input_data is a square matrix
jump = 0;
new_jump = 0;
output_data = input_data;

for(ii=1:sz(1))
    for(jj=1:sz(2))
        if (jj-jump < 1)
            new_jump = sz(2)-jump+(jj);
%             tmp = (ii,new_jump);
            output_data(ii,new_jump) = input_data(ii,jj);
        else
            output_data(ii,jj-jump) = input_data(ii,jj);
%         tmp = input_data(ii,jj-jump);
        end
    end
    jump = jump + 1;
end
output_data;

end
