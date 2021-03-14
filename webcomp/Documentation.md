# Documentation

---
This tool takes two URLs as an input and calculates a similarity score, that represents the suspicious similarity of these two websites. This is done using different features of the websites. Those features include content, domain, links, image sources and the screenshots of the websites.

---

## Content
If a website is designed to fool people, the content must be the same or at least very similar. For example on websites like Facebook, Instagram and so on, people are looking for a `Username` and `Password` login field, thus it must be somewhere on the page. Content like this is covered in this feature. Both websites are crawled and the HTML-markup is removed. What's left over is the content of the websites that now will be compared line by line. It checks how many lines of website A are also given in website B and the other way around. The sum of both found lines is then divided by the sum of all lines. This gives the first percentage of similarity.

## Domain
Although the normal user does not really have a look at the domain it should be considered anyway. If a website clone should lead people to put in their credentials the domain should be similar to the original one as well. That's why domain comparison is the second percentage we calculate. The tool takes the two given URLs and removes the protocol (https:// or http://) and also the directory path and queries. What's left over is the real domain like for example `www.google.com`. Those two domains are now split into their components which then are compared in the same way like the lines of content. The result is our second similarity percentage.

## Links
Another very interesting component of websites are links, that point to other websites, images or sub directories. The tool searches for them in both websites and again compares them with each other. Doing so, we get the third similarity percentage.

## Image Sources
This component basically is the same as Links but with image sources. As well as the other links, they are collected and compared to each other, giving us the fourth similarity percentage.

## Screenshots
The last component is the comparison of the screenshots of both websites. For that the tool first creates a screenshot of both websites and then compares them with each other. Therefor it uses two different image comparison ideas implemented in three algorithms.

### Idea 1
Here each pixel will be compared with the corresponding pixel of the other image. For that to work it is important to scale the images correctly. Therefore a function is implemented, that scales the second given image like the first one. Then both are compared pixel by pixel.
  - *MSE*
    - This stands for Mean Squared Error and is simply a sum over squares of the differences per each single pixel in the images.
  - *imgcompare.image_diff_percent*
    - This basically does the same calculation like MSE but without the squared component.


### Idea 2 
Here the image won't be compared pixel by pixel but in bigger groups of pixels. This is helpful considering the same image but one time scaled a little bigger. While Idea 1 would score worse on images like this, this approach works much better.
  - *SSIM*
    - This stands for Structural Similarity Algorithm and is an exact implementation of Idea 2.


We chose MSE because it is easy to use and to implement while giving good results in similar images. imgcompare.image_diff_percent was chosen because it does the same thing but in a slightly different way. So two references are better then one. We chose the SSIM algorithm because it comes in a library, thus it is super easy to use and brings good results in comparing images that are more different.

The main Problem in this feature basically is the weakness of colors. That means, that in all implemented algorithms the color of the website has an huge impact of how similar they think the websites are. That means, that the same website in two different colors would have a smaller similarity score than two different websites having the same color. That's because those algorithms do not recognize patterns in images like Convolutional Neural Networks do. So to get better results one should try training a CNN for image recognition to fulfill this task in a better way.

## Calculation of Similarity Score
At this point the tool has 5 percentages, each of them stating how similar the two websites are, considering their features. Now the final similarity score is calculated in the following way:

Each feature has a maximum of 2 similarity points to give. That means, if the percentage is higher than or equal to a set threshold, the full 2 points are given for this feature. If the percentage is smaller then the threshold, the points are calculated based on a percentage elimination.

**Here is a short example:** Let's consider a percentage of `0.34` and a threshold of `0.4`. Clearly 0.34 is smaller than 0.4 so it won't achieve 2 points. We now define a percentage x = `0.2`. This is now used for calculating the points:

Since 0.34 is smaller than 0.4 we will now subtract x * threshold from the original threshold. That means that the new threshold is `0.34 - (0.2 * 0.34) = 0.272`. For each of those iterations the maximum similarity points get decreased by `0.5`. Since `0.34` is now greater than `0.272` the requirement is fulfilled and the feature would achieve `1.5` similarity points.

This procedure is done for each feature and the final similarity score is the sum of all calculated points.

## Changing the manner of the project
If you want to modify the functionality of our tool to be used in another way or simply improve it, you have the following options:

- Set different thresholds for each feature
- Come up with another way of calculating points for each feature
- Come up with a new scoring system
- Use trained CNNs for image comparison
- Add new features like CSS or font comparison
