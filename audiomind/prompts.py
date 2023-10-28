PROMPT_TEMPLATES = {
    "summary_template": """Based on the provided transcript which is unstructured and chaotic, generate a detailed recap in bullet-point format. 
    Capture all the topics discussed exhaustively. 
    Group the bullet points into sections only if the topics naturally fall under a specific category. 
    If possible, include examples to highlight key points discussed.
Transcript:

{text}

Use Markdown. Add ## for section titles.""",

"notes_template": """
You are an expert copywriter. People gives you transcripts of their voice notes and you have to convert them into meaningful notes.
The voice note might be a journal entry, a meeting, a lecture, a podcast, etc. 
It is very unstructured and chaotic. 

I will give you the transcript of the voice note under [Transcript]
and details about the person who recorded it under [Person].

The reader is the same person, so you can use the details to personalize the notes but it is not necessary.
Dont unnecassarily use the person details in the notes.
Keep info in first person from the perspective of the person who recorded the voice note if possible and appropriate.
Transform the transcript into concise and structured notes, 
highlighting the key points and breakthroughs discussed.

Follow the chain of thought of the speaker and capture all the topics discussed exhaustively.
Dont make any assumptions. Dont add any extra information in the notes.

Dont make key points a long list of bullet points only. 
Group the thoughts or transcript into sections, and then add bullet points under each section.
Keep the order of the sections same as the order of the topics discussed in the transcript or their importance.

Include all action items and reflections 
Also, Create single section for action items / to-dos form the transcript and add them at the end of the notes.
Make sure to organize the information logically and eliminate any repetitive or irrelevant details.

[Transcript]
{text}
[Person]
{details}

Dont add any extra information in the notes.
I will create a title for journal myself. Dont add a heading / title in the notes.
Use Markdown. Add ## for section titles.
""",

"meeting_template": """
You are an expert copywriter. People gives you transcripts of their voice notes and you have to convert them into meaningful notes.
The voice note might be a journal entry, a meeting, a lecture, a podcast, etc. 
It is very unstructured and chaotic. 

I will give you the transcript of the meeting under [Transcript]
and details about the person who recorded it under [Person].

Dont unnecassarily use the person details in the notes.
Transform the transcript into concise and structured notes, 
highlighting the key points and breakthroughs discussed.

Follow the chain of thought of the speaker and capture all the topics discussed exhaustively.
Dont make any assumptions. Dont add any extra information in the notes.

Dont make key points a long list of bullet points only. 
Group the thoughts or transcript into sections, and then add bullet points under each section.
Keep the order of the sections same as the order of the topics discussed in the transcript or their importance.

Include all action items and reflections at the end of the notes..
Make sure to organize the information logically and eliminate any repetitive or irrelevant details.

[Transcript]
{text}
[Person]
{details}

Dont add any extra information in the notes.
I will create a title for journal myself. Dont add a heading / title in the notes.
Use Markdown. Add ## for section titles.
""",

    "title_description_template": """
I will give you notes in the form of a summary. It can be a journal entry, meeting notes or something else.
notes are divided into sections with bullet points with every section being a key point discussed in the notes.
Finally, it can consist of a list of action items / to-dos. Dont give action items and to-dos any priority in the title and description.
Your job is to generate single title and description for the notes.
write a short title and description, separate both by \n\n
Keep the title as short as possible, and make it a single line. Keep title below 100 characters.
The description should be a single paragraph. Keep description below 250 characters.

Text:
{text}
        
Return a Markdown in below format:
# TITLE HERE
#### DESCRIPTION HERE
""",
}
