import re


class CreativityTracker:
    def __init__(
        self,
        word_overuse_threshold,
    ):
        self.words_used = {}
        self.stop_words = {
            "a",
            "an",
            "and",
            "are",
            "as",
            "at",
            "be",
            "by",
            "has",
            "he",
            "in",
            "is",
            "it",
            "of",
            "on",
            "that",
            "the",
            "to",
        }
        self.word_overuse_threshold = word_overuse_threshold

    def _get_preprocessed_words_in_action(self, action: str):
        # convert to lowercase
        action = action.lower()
        # remove special characters
        action = re.sub(r"[^a-z\s]", "", action)
        # split into words
        words = action.split()
        # Remove common stop words
        words = [word for word in words if word not in self.stop_words]

        return words

    def add_action(self, action: str):
        for word in self._get_preprocessed_words_in_action(action):
            self.words_used[word] = self.words_used.get(word, 0) + 1

    def count_new_words_in_action(self, action: str):
        new_words = 0
        words_in_action = set(self._get_preprocessed_words_in_action(action))
        for word in words_in_action:
            if word not in self.words_used:
                new_words += 1
        return new_words

    def count_overused_words_in_action(self, action: str):
        overused_words = 0
        for word in self._get_preprocessed_words_in_action(action):
            if word in self.words_used:
                amount_used = self.words_used[word]
                if amount_used >= self.word_overuse_threshold:
                    overused_words += 1
        return overused_words
