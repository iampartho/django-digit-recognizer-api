import cv2


### utility function for calculating row black and white pixels ####

def count_black_white_row(width_seg, height, char_seg):
    white_row = []
    black_row = []
    white_max_row = 0
    black_max_row = 0
    for i in range(height):
        white_count = 0
        black_count = 0
        for j in range(width_seg):
            if char_seg[i][j] == 0:
                black_count += 1
            else:
                white_count += 1

        white_row.append(white_count)
        black_row.append(black_count)

    white_max_row = max(white_row)
    black_max_row = max(black_row)
    return white_row, black_row, white_max_row, black_max_row

# finding the ending edge of the character in column
def find_end(start_col, width, white_col,white_max_col, segmentation_spacing):
    end_col = start_col + 1
    for m in range(start_col + 1, width - 1):
        if(white_col[m] > segmentation_spacing * white_max_col):
            end_col = m
            break
    return end_col

# finding the ending edge of the character in row
def find_end_row(start_row, height, white_row,white_max_row, segmentation_spacing):
    
    end_row = start_row + 1
    for m in range(start_row + 1, height - 1):
        if(white_row[m] > segmentation_spacing * white_max_row):
            end_row = m
            break

    return end_row

def segments_image(img):
	# threshold to select a column where the character started
	segmentation_spacing = 0.99

	# image pre-processing before segmentation
	img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

	blur = cv2.GaussianBlur(img, (5,5), 0)

	ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

	# calculate black and white pixels in each column

	white_col = []  # Record the sum of white pixels in each column
	black_col = []  # Record the sum of black pixels in each column



	height = thresh.shape[0]
	width = thresh.shape[1]

	white_max_col = 0
	black_max_col = 0




	'''4 Cycle through the sum of black and white pixels for each column'''
	for i in range(width):
	    white_count = 0
	    black_count = 0
	    for j in range(height):
	        if thresh[j][i] == 0:
	            black_count += 1
	        else:
	            white_count += 1

	    white_col.append(white_count)
	    black_col.append(black_count)

	white_max_col = max(white_col)
	black_max_col = max(black_col)

	n = 1 # column counter
	k = 1 # row counter
	start_col = 1
	end_col = 2

	digit = []
	while n < width - 1:
	    n += 1
	    if(black_col[n] > (1 - segmentation_spacing) * black_max_col):
	        start_col = n
	        end_col = find_end(start_col, width, white_col,white_max_col, segmentation_spacing)
	        n = end_col 
	        if end_col - start_col > 5:
	            
	            character_seg = thresh[1:height, start_col-10:end_col+10]
	            h, w = character_seg.shape
	            white_row, black_row, white_max_row, black_max_row = count_black_white_row(w,h,character_seg)
	            
	            while k < h-1:
	                k += 1
	                if (black_row[k] > (1 - segmentation_spacing) * black_max_row):
	                    start_row = k
	                    end_row = find_end_row(start_row, h, white_row,white_max_row, segmentation_spacing)
	                    break
	            k=1
	            
	            character = img[start_row-10:end_row+10, start_col-10:end_col+10]
	            character = cv2.resize(character, (28,28), interpolation=cv2.INTER_CUBIC)
	            digit.append(character)


	return digit





