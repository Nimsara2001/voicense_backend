from typing import Optional
from pydantic import BaseModel, Field


class Transcription(BaseModel):
    transcription_id: str = Field(...)
    content: str = Field(...)
    generated_date: str = Field(...)
    note_id: str

    class Config:
        json_schema_extra = {
            "example": {
                "transcription_id": "VSCT0001",
                "content": " Hello, my name is Chandu Nair and I am going to be handling the subject of marketing management. Marketing is a fascinating subject, a fairly new subject and I am sure all of you will learn quite a bit as we go along. In this chapter, we will cover a host of things. At the end of this chapter, you will understand what exactly is meant by marketing management. What a market is, we all have very many doubts, many views on what a market is, but by the end of this chapter, you will get a much better sense of what all definitions exist around a market. Thirdly, you will get a better understanding of the various concepts of marketing. Fourthly, a very common misconception is the difference between marketing and selling. Many people assume they are the same. By the end of this chapter, you will understand that it is not the same. Fifthly, you will get an understanding of the marketing management process, the importance and the role of marketing in the Indian context. And finally, how does one develop a marketing orientation? Now, many of us think marketing is fairly new, yes it is as a discipline, but in actuality, it is as old as civilization itself. Many people believe the first exchange actually took place between Adam and Eve. So, that gives you an idea of how old marketing is. In fact, many people believe it is almost like the oldest profession, because marketing is all about the exchange of ideas and an exchange of communication. But the first signs of organized communication happened actually post the Industrial Revolution. And the real evolution of marketing as a discipline happened much later in the 20th century and the first seminal work happened late 60s, early 70s with Philip Coattler's seminal book on marketing management. Today, many people who confuse marketing and equated it with selling in the past realize that they are very different and marketing is a much, much wider and much more acceptable term. So, in the past people in the olden days first started producing something and then realized that they needed something else from somebody else. So, which is how the concept of barter or exchange is started. Subsequently, as the Industrial Revolution came, a lot of goods started getting produced and people found that they are much more than what was required or demanded, which is when things the concept of selling happened. People also started to figure out a little bit as they went along of what consumers wanted and then they found the first salesman appearing. And thereafter in the 50s and 60s the golden age when people look back the golden age of advertising and of marketing the first brand managers started appearing. Product management started becoming popular, but it is after the 70s that marketing really came into its own. But the end of the 80s people realized that even the old marketing theory needed substantial revamp and today in the day of the internet, in the day of virtual market places, in the day of e-commerce there is a new marketing theory that has been propounded. And that is what this particular slide tells you what all has happened over the last several decades. Now, we come to the core which is what is marketing management. There are two definitions out here, one the very old definition from the American Marketing Association, which says that marketing management is the performance of business activities that direct the flow of goods and services from producer to consumer or user. Now, a lot of people find this a very limiting definition because it only talks about things which are produced and it only seems to focus a lot on the physical distribution of things from one producer to another consumer. So, a lot of people prefer the second definition which is a much wider definition, the one propounded by Philip Kotler, where he said it is societal process by which individuals and groups obtain what they need and want through creating, offering and freely exchanging products and services of value to each other. Marketing is an ongoing process of discovering and translating consumer needs and desires into products and services, creating demand for these products and services, serving the consumers and is demand through a network of marketing channels and expanding the market to base in the face of competition. As you can make out this definition covers a whole host of activities, covers a whole host of intermediaries and players and covers a whole gamut of aspects, emotions, feelings, wants, desires, fulfilment and so on. This is what people believe contributes more to marketing management than the traditional and more outdated definition that the AMA has propounded. So, the next big question for many of us in India, a market typically means a physical place where people meet and exchange goods or products or services. Well, that was in the past, but today a marketplace can be virtual. eBay for example, is a very good marketplace which barely exists on the ground, it exists virtually. There are several such marketplaces which do not exist at all in the physical world, but seem to have a very tremendous presence in today's time and age. So, if you look at this is the traditional definition of a market, but a new definition is a potential set of buyers and sellers who offer some value to consumers. So, this brings us to a very important aspect, what marketing concepts underlie this definitions of a market and this definition of marketing management. Now, a lot of people really do not understand that they have different assumptions and this set of concepts that are going to be placed in the next slide will give you an idea of the different assumptions that people operate from. For example, there are still a whole bunch of people who believe in the production concept, which is that all you need to do is produce and then somehow there will be customers who need what you are producing and the focus therefore, is on producing more and more with the assumption that the more I produce the more profitable my business will be. The second one is the product concept and this is based on the old saying that if you build a better mouse trap the world will beat the path to your door no longer true in the sense the focus here is on developing a superior product. Now, as you have seen there are enough and more examples of companies who have built products, but have actually failed in the marketplace as compared to companies who have built products which customers lapped up. A good example is Microsoft and its windows operating system a lot of people believe it is not the best operating system it did not have the best applications, but still it was the most successful in its marketplace. The third is selling the selling concept people believe in this concept that a lot of customers would not really buy on their own accord and they somehow need to be persuaded to buy. This is very common among those with a very trading and transactional mentality. The fourth concept which is what is more and more getting accepted is the marketing concept which is that your success as a company lies in your ability to distinguish yourself from your competitor by offering a better value proposition to your customers. So, here the concept is comparing yourself with what the competition is offering and doing a better job of it. Now, the final thing in these days of environmental consciousness and being more socially aware is the societal marketing concept which says not only must you have a better value proposition, but it must also be socially relevant and desirable. So, for example, you will find that in India smoking or cigarette selling or promotions are banned. Similarly, you cannot also promote advertised liquor so easily because in the eyes of many such products are really not especially smoking or really not what is desirable from a society's point of view. So, one must keep into account take into account the larger good of the society when one is marketing. So, as you can make out there are different assumptions in each of these concepts and it is wise for you to ponder what concepts many companies that you see around are using when they are selling or marketing their products.",
                "generatedDate": "2024-05-21",
                "note_id": "VSCN0001"
            }
        }

