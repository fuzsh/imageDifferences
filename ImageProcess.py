from skimage.measure import compare_ssim

import imutils
import cv2


def image_process(user_id):
    main_image = cv2.imread(str(user_id) + '.jpg')
    new_x, new_y = main_image.shape[1], main_image.shape[0]

    if int(new_x) % 2 != 0:
        new_x += 1
    if int(new_y) % 2 != 0:
        new_y += 1

    main_image = cv2.resize(main_image, (int(new_x), int(new_y)))

    height, width = main_image.shape[:2]
    width_cutoff = width // 2

    first_image = main_image[:, :width_cutoff]
    second_image = main_image[:, width_cutoff:]

    first_image_gray = cv2.cvtColor(first_image, cv2.COLOR_BGR2GRAY)
    second_image_gray = cv2.cvtColor(second_image, cv2.COLOR_BGR2GRAY)

    (score, diff) = compare_ssim(first_image_gray, second_image_gray, full=True)
    diff = (diff * 255).astype("uint8")

    thresh = cv2.threshold(diff, 0, 255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if imutils.is_cv2() else contours[1]

    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(first_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(second_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imwrite("./ToUserSend/First-" + str(user_id) + ".jpg", first_image)
    cv2.imwrite("./ToUserSend/Second-" + str(user_id) + ".jpg", second_image)
    cv2.imwrite("./ToUserSend/Different-" + str(user_id) + ".jpg", diff)
    cv2.imwrite("./ToUserSend/Thresh-" + str(user_id) + ".jpg", thresh)

    return score

