from audiomind import AudioMind

def test_audiomind_initialization():
    # Given a sample file path
    sample_file = "path/to/sample/audio/file.mp3"
    base_name = AudioMind.get_main_file_name(sample_file)

    # When an AudioMind instance is created
    mind = AudioMind(file=sample_file)

    # Then the instance should be of type AudioMind and have the given file path
    assert isinstance(mind, AudioMind)
    assert mind.file == sample_file
    assert mind.base_name == base_name
