def feature_extractor(filename):
    '''
    input params: 
    filename : path of the file that we want to process

    Output params:
    l : Feature vector
    '''

    try:
        main_img = cv2.imread(filename)
        img = cv2.cvtColor(main_img, cv2.COLOR_BGR2RGB)
    except:
        return "Invalid"

    #Preprocessing
    

    gs = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gs, (25,25),0)
    ret_otsu,im_bw_otsu = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    kernel = np.ones((25,25),np.uint8)
    closing = cv2.morphologyEx(im_bw_otsu, cv2.MORPH_CLOSE, kernel)

    #Shape features
    contours, _ = cv2.findContours(closing,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    M = cv2.moments(cnt)
    area = cv2.contourArea(cnt)
    if area==0:
        return "Invalid"
    perimeter = cv2.arcLength(cnt,True)

    current_frame = main_img
    filtered_image = closing/255

    #Elementwise Multiplication of range bounded filtered_image with current_frame
    current_frame[0:current_frame.shape[0], 0:current_frame.shape[1], 0] = np.multiply(current_frame[0:current_frame.shape[0], 0:current_frame.shape[1], 0], filtered_image) #B channel
    current_frame[0:current_frame.shape[0], 0:current_frame.shape[1], 1] = np.multiply(current_frame[0:current_frame.shape[0], 0:current_frame.shape[1], 1], filtered_image) #G channel
    current_frame[0:current_frame.shape[0], 0:current_frame.shape[1], 2] = np.multiply(current_frame[0:current_frame.shape[0], 0:current_frame.shape[1], 2], filtered_image) #R channel

    img = current_frame


    #standard deviation for colour feature from the image.    
    red_std = np.std(red_channel)
    green_std = np.std(green_channel)
    blue_std = np.std(blue_channel)

     #Color features
    red_channel = img[:,:,0]
    green_channel = img[:,:,1] #show the intensities of green channe
    blue_channel = img[:,:,2]

    red_mean = np.mean(red_channel)
    green_mean = np.mean(green_channel)
    blue_mean = np.mean(blue_channel)



    
    
    #amt.of green color in the image
    gr = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    boundaries = [([30,0,0],[70,255,255])]
    for (lower, upper) in boundaries:                                                                 #to check the color
        mask = cv2.inRange(gr, (36, 0, 0), (70, 255,255))
        ratio_green = cv2.countNonZero(mask)/(img.size/3)
        f1=np.round(ratio_green, 2)
    #amt. of non green part of the image   
    f2=1-f1

    
    #with the help of glcm find the contrast
    contrast = greycoprops(g, 'contrast')
    f4=contrast[0][0]+contrast[0][1]+contrast[0][2]+contrast[0][3]
    #[0][3] represent no. of times grey level 3 appears at the right of 0


    #Texture features using grey level cooccurance matrix
    img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    g=greycomatrix(img, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4])

    



    #help of glcm find the homogeneity
    homogeneity = greycoprops(g, prop='homogeneity')
    f6=homogeneity[0][0]+homogeneity[0][1]+homogeneity[0][2]+homogeneity[0][3]

    #to  help of glcm find the energy.   
    energy = greycoprops(g, prop='energy')
    f7=energy[0][0]+energy[0][1]+energy[0][2]+energy[0][3]

    # help of glcm find the dissimilarity 
    dissimilarity = greycoprops(g, prop='dissimilarity')
    f5=dissimilarity[0][0]+dissimilarity[0][1]+dissimilarity[0][2]+dissimilarity[0][3]

    #help of glcm find the correlation    
    correlation = greycoprops(g,prop= 'correlation')
    f8=correlation[0][0]+correlation[0][1]+correlation[0][2]+correlation[0][3]



    l = [area, perimeter, red_mean, green_mean, blue_mean,
         f1, f2, red_std, green_std, blue_std,
        f4,f5,f6,f7,f8]
    return l
