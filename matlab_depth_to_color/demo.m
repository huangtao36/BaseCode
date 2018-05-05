

file = './688_real_B.png';
I = imread(file);
D_est = double(I)/256;
D_est(I==0) = -1;

color_image = disp_to_color(D_est);

imwrite(color_image, './color_688_real_B.png')

% figure,imshow(color_image);
