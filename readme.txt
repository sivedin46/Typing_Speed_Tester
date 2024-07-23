1--i used frames for user interface.
2--count_down function:
    everytime it called with count=60 it creates a 60 seconds timer. after finishing 60 seconds calls  check_record()
        update_display() and writes 0 for time info.
        check_records() checks if the user typed more than record word count. if true writes new record to records.txt
         file and writes new record to main window.
         update_display() deletes last infos fow Word per minute and correct for minute.
         Also disables event triggering keys space and enter to not to call compare function.
3---start_timer() function actuaaly starts typing exercise:
    first it cancelles if an still going timer exists
    then reads record from records.txt with read_record()
    after that it calls  initialize_all() for first initialition of some widgets and infos and variables
    enables for space and enter keys for starting exercise for triggereing compare function
    clears tags for red and green texts
    clears and enables user text entry
4------initialize_all()
5-----open_sample_text() function gives opportinity tu user for upload its own text for studying
    after uploading it makes for some modifications over text and writes to screen.
    After writing screen it disables screen to protect entered sample text
6.------compare(event)   this is our main function. It compares the tyed word with sample word.
        If tyed word correct,  it changes color to green else the word is red.
        ıt counts all correct words and all typed words.
        our event occurs only when space or return key pressed. Why when user presses this keys it means he typed a word.
        all comparisions done till all words in sample text is finished.
        If you type a wrong char in word. whole word turns red not the char. It makes this with controlling word lenght
        of sample word not the user input word.
             end_index = f"1.{char_counter + len(sample_words[counter])}"
            sample_text.tag_add(state, start_index, end_index)
            char_counter += len(sample_words[counter]) + 1  # +1 for the space
            counter += 1

