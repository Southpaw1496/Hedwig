package template.extensions

import com.kotlindiscord.kord.extensions.extensions.Extension
import dev.kord.common.annotation.KordPreview

@OptIn(KordPreview::class)
class TestExtension : Extension() {
    override val name = "test"

    override suspend fun setup() {
    }

}